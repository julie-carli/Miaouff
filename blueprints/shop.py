"""Shopping cart, checkout, Stripe payment and order management."""

from datetime import datetime

import stripe
from flask import (
    Blueprint,
    current_app,
    flash,
    jsonify,
    redirect,
    render_template,
    request,
    session,
    url_for,
)
from flask_login import current_user, login_required

from models.models import Order, OrderProduct
from models.models import Payment as PaymentModel
from models.models import Product, User, db
from services.cart_service import (
    add_to_cart,
    get_cart,
    get_cart_count,
    get_cart_totals,
    is_address_complete,
    remove_from_cart,
    update_cart,
)

shop_bp = Blueprint("shop", __name__)


@shop_bp.route("/cart")
def cart():
    cart_items = get_cart(session)
    totals = get_cart_totals(cart_items)
    return render_template("cart.html", cart=cart_items, totals=totals)


@shop_bp.route("/add_to_cart/<int:product_id>", methods=["POST"])
def add_to_cart_route(product_id):
    data = request.get_json()
    quantity_requested = int(data.get("quantity", 1))
    success, message = add_to_cart(session, product_id, quantity_requested)
    if not success:
        return jsonify({"success": False, "message": message}), 400
    return jsonify({"success": True, "cart_count": get_cart_count(session)})


@shop_bp.route("/update_cart/<int:product_id>", methods=["POST"])
def update_cart_route(product_id):
    data = request.get_json()
    new_quantity = int(data.get("quantity", 1))
    success, message, corrected = update_cart(session, product_id, new_quantity)
    if not success:
        return (
            jsonify(
                {
                    "success": False,
                    "message": message,
                    "corrected_quantity": corrected,
                    "cart_count": get_cart_count(session),
                }
            ),
            400,
        )
    return jsonify({"success": True, "cart_count": get_cart_count(session)})


@shop_bp.route("/remove_from_cart/<int:product_id>", methods=["POST"])
def remove_from_cart_route(product_id):
    remove_from_cart(session, product_id)
    return redirect(url_for("shop.cart"))


@shop_bp.route("/check_order")
@login_required
def check_order():
    """Entry point for the checkout flow.

    Redirects to address edit if the address is incomplete, otherwise shows
    the order summary.
    """
    user = User.query.get(current_user.user_id)
    cart_items = get_cart(session)

    if not cart_items:
        flash("Votre panier est vide.", "danger")
        return redirect(url_for("shop.cart"))

    if not is_address_complete(user):
        flash("Veuillez compléter votre adresse de livraison.", "danger")
        return redirect(url_for("shop.edit_address"))

    totals = get_cart_totals(cart_items)
    return render_template(
        "check_order.html", cart=cart_items, user=user, totals=totals
    )


@shop_bp.route("/payment", methods=["GET", "POST"])
@login_required
def payment():
    """GET: display the Stripe payment form.

    POST: create a Stripe PaymentIntent and return the client_secret.
    """
    cart_items = get_cart(session)
    if not cart_items:
        return redirect(url_for("shop.cart"))

    totals = get_cart_totals(cart_items)

    if request.method == "POST":
        # Amount must be in cents (integer) for Stripe
        amount_cents = int(totals["grand_total"] * 100)
        try:
            intent = stripe.PaymentIntent.create(
                amount=amount_cents,
                currency="eur",
                metadata={"user_id": current_user.user_id},
            )
            return jsonify({"client_secret": intent.client_secret})
        except stripe.error.StripeError as e:
            return jsonify({"error": str(e)}), 400

    return render_template(
        "payment.html",
        totals=totals,
        stripe_public_key=current_app.config["STRIPE_PUBLIC_KEY"],
    )


@shop_bp.route("/payment_success", methods=["POST"])
@login_required
def payment_success():
    """Called by the frontend after Stripe confirms the payment.

    Creates Order, OrderProduct and Payment records, then clears the cart.
    """
    cart_items = get_cart(session)
    if not cart_items:
        return jsonify({"success": False}), 400

    totals = get_cart_totals(cart_items)
    user = User.query.get(current_user.user_id)

    # Create the order record
    order = Order(
        user_id=user.user_id,
        order_date=datetime.now(),
        status="paid",
        total_price_excl_tax=totals["total_excl_tax"],
        total_price_incl_tax=totals["total_incl_tax"],
        shipping_fee=totals["shipping_fee"],
    )
    db.session.add(order)
    db.session.flush()  # Needed to get order.order_id before commit

    # Create one OrderProduct line per cart item and decrement stock
    for item in cart_items:
        product_obj = Product.query.get(item["product_id"])
        if product_obj:
            op = OrderProduct(
                order_id=order.order_id,
                product_id=item["product_id"],
                quantity=item["quantity"],
                unit_price_excl_tax=round(item["price"] / 1.20, 2),
                unit_price_incl_tax=item["price"],
            )
            db.session.add(op)
            product_obj.stock = max(0, product_obj.stock - item["quantity"])

    # Create the payment record
    payment_record = PaymentModel(
        payment_method="card",
        payment_status="paid",
        payment_date=datetime.now(),
        payment_total=totals["grand_total"],
        order_id=order.order_id,
    )
    db.session.add(payment_record)
    db.session.commit()

    # Clear the session cart
    session["cart"] = []
    session.modified = True

    return jsonify({"success": True, "order_id": order.order_id})


@shop_bp.route("/order_confirmation/<int:order_id>")
@login_required
def order_confirmation(order_id):
    """Show the order confirmation page after successful payment."""
    order = Order.query.get_or_404(order_id)
    # Security: a user can only see their own order confirmation
    if order.user_id != current_user.user_id:
        return redirect(url_for("main.home"))
    return render_template("order_confirmation.html", order=order)


@shop_bp.route("/order/<int:order_id>")
@login_required
def order_detail(order_id):
    """Show full details of a specific order, accessible only by its owner."""
    order = Order.query.get_or_404(order_id)
    if order.user_id != current_user.user_id:
        return redirect(url_for("auth.account"))
    return render_template("order_detail.html", order=order)


@shop_bp.route("/edit_address", methods=["GET", "POST"])
@login_required
def edit_address():
    """Let the user fill in or update their delivery address."""
    user = User.query.get(current_user.user_id)

    if request.method == "POST":
        user.first_name = request.form.get("first_name")
        user.last_name = request.form.get("last_name")
        user.address_number = request.form.get("address_number")
        user.street_name = request.form.get("street_name")
        user.address_complement = request.form.get("address_complement")
        user.postal_code = request.form.get("postal_code")
        user.city = request.form.get("city")
        user.country = request.form.get("country")
        user.phone = request.form.get("phone")
        db.session.commit()
        flash("Adresse mise à jour.", "success")
        return redirect(url_for("shop.check_order"))

    return render_template("edit_address.html", user=user)
