from models.models import Product


def get_cart(session):
    """Retrieve the current cart from the session."""
    return session.get("cart", [])


def add_to_cart(session, product_id, quantity_requested):
    """
    Add a product to the cart or update its quantity if already present.
    Prices are cast to float to avoid Decimal serialization issues.
    Returns (success: bool, message: str).
    """
    product = Product.query.get(product_id)
    if not product:
        return False, "Produit introuvable."

    price = float(product.price_incl_tax)
    cart = get_cart(session)

    # Update quantity if product is already in the cart
    for item in cart:
        if item["product_id"] == product_id:
            total_quantity = item["quantity"] + quantity_requested
            if total_quantity > product.stock:
                return False, "Stock insuffisant."
            item["quantity"] = total_quantity
            item["total_price"] = round(item["quantity"] * item["price"], 2)
            session["cart"] = cart
            session.modified = True
            return True, "Quantité mise à jour."

    # Check stock before adding new item
    if quantity_requested > product.stock:
        return False, "Stock insuffisant."

    cart.append({
        "product_id": product_id,
        "name": product.name,
        "price": price,
        "quantity": quantity_requested,
        "total_price": round(quantity_requested * price, 2),
        "image": product.image,
        "stock": product.stock,
    })
    session["cart"] = cart
    session.modified = True
    return True, "Produit ajouté au panier."


def update_cart(session, product_id, new_quantity):
    """
    Update the quantity of a product already in the cart.
    Returns (success: bool, message: str, corrected_quantity: int or None).
    """
    cart = get_cart(session)

    for item in cart:
        if item["product_id"] == product_id:
            product = Product.query.get(product_id)
            if new_quantity > product.stock:
                return False, "Stock insuffisant.", product.stock
            item["quantity"] = new_quantity
            item["total_price"] = round(new_quantity * item["price"], 2)
            session["cart"] = cart
            session.modified = True
            return True, "Panier mis à jour.", None

    return False, "Produit non trouvé.", None


def remove_from_cart(session, product_id):
    """Remove a product from the cart entirely."""
    cart = get_cart(session)
    session["cart"] = [item for item in cart if item["product_id"] != product_id]
    session.modified = True


def is_address_complete(user):
    """
    Check that all required address fields are filled before proceeding to payment.
    """
    return all([
        user.first_name,
        user.last_name,
        user.address_number,
        user.street_name,
        user.postal_code,
        user.city,
        user.country,
    ])


def get_cart_totals(cart):
    """
    Compute cart summary: total excl. tax, total incl. tax, shipping fee, grand total.
    Tax rate assumed at 20%. Shipping is free above 50€ TTC.
    Returns a dict with all totals as floats.
    """
    total_incl_tax = round(sum(float(item["total_price"]) for item in cart), 2)
    # Back-calculate excl. tax from incl. tax (TVA 20%)
    total_excl_tax = round(total_incl_tax / 1.20, 2)
    shipping_fee = 0.0 if total_incl_tax >= 50 else 5.90
    grand_total = round(total_incl_tax + shipping_fee, 2)

    return {
        "total_excl_tax": total_excl_tax,
        "total_incl_tax": total_incl_tax,
        "shipping_fee": shipping_fee,
        "grand_total": grand_total,
    }