from models.models import Product


def get_cart(session):
    """Retrieve the current cart from the session."""
    return session.get("cart", [])


def add_to_cart(session, product_id, quantity_requested):
    """
    Add a product to the cart or update its quantity if already present.
    Returns (success: bool, message: str).
    """
    product = Product.query.get(product_id)
    if not product:
        return False, "Produit introuvable."

    cart = get_cart(session)

    # Update quantity if product is already in the cart
    for item in cart:
        if item["product_id"] == product_id:
            total_quantity = item["quantity"] + quantity_requested
            if total_quantity > product.stock:
                return False, "Stock insuffisant."
            item["quantity"] = total_quantity
            item["total_price"] = item["quantity"] * item["price"]
            session["cart"] = cart
            return True, "Quantité mise à jour."

    # Check stock before adding new item
    if quantity_requested > product.stock:
        return False, "Stock insuffisant."

    cart.append({
        "product_id": product_id,
        "name": product.name,
        "price": product.price_incl_tax,
        "quantity": quantity_requested,
        "total_price": quantity_requested * product.price_incl_tax,
        "image": product.image,
    })
    session["cart"] = cart
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
            item["total_price"] = new_quantity * item["price"]
            session["cart"] = cart
            return True, "Panier mis à jour.", None

    return False, "Produit non trouvé.", None


def remove_from_cart(session, product_id):
    """Remove a product from the cart entirely."""
    cart = get_cart(session)
    session["cart"] = [item for item in cart if item["product_id"] != product_id]


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