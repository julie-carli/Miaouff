from models.models import db, Product, Category


def get_products_by_category(category_name=None):
    """
    Return all products, or filter by category name if provided.
    Returns a tuple (products_list, categories).
    """
    categories = Category.query.order_by(Category.name.asc()).all()

    if category_name:
        selected_category = Category.query.filter_by(name=category_name).first()
        products_list = (
            Product.query.filter_by(category_id=selected_category.category_id).all()
            if selected_category
            else []
        )
    else:
        products_list = Product.query.all()

    return products_list, categories


def save_or_update_product(form_data, product=None):
    """Create a new product or update an existing one."""
    name = form_data["name"]
    description = form_data.get("description", "")
    price_excl_tax = form_data["price_excl_tax"]
    price_incl_tax = form_data["price_incl_tax"]
    stock = form_data["stock"]
    weight = form_data["weight"]
    image = form_data.get("image", "")
    category_id = form_data.get("category_id")

    if product:
        product.name = name
        product.description = description
        product.price_excl_tax = price_excl_tax
        product.price_incl_tax = price_incl_tax
        product.stock = stock
        product.weight = weight
        product.image = image
        product.category_id = category_id
    else:
        product = Product(
            name=name,
            description=description,
            price_excl_tax=price_excl_tax,
            price_incl_tax=price_incl_tax,
            stock=stock,
            weight=weight,
            image=image,
            category_id=category_id,
        )
        db.session.add(product)

    db.session.commit()
    return product


def delete_product(product_id):
    """Delete a product by ID."""
    product = Product.query.get_or_404(product_id)
    db.session.delete(product)
    db.session.commit()


def add_category(name):
    """Add a new category if the name is not empty."""
    if name:
        category = Category(name=name)
        db.session.add(category)
        db.session.commit()
        return category
    return None


def update_category(category_id, new_name):
    """Update an existing category's name."""
    category = Category.query.get_or_404(category_id)
    category.name = new_name
    db.session.commit()
    return category


def delete_category(category_id):
    """Delete a category by ID."""
    category = Category.query.get_or_404(category_id)
    db.session.delete(category)
    db.session.commit()