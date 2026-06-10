"""Admin back office: CRUD for users, shelters, animals, pets, products,
categories and blog articles. Every route requires an authenticated admin."""

import os
import re
from datetime import datetime
from functools import wraps

from bson import ObjectId
from flask import (
    Blueprint,
    current_app,
    flash,
    redirect,
    render_template,
    request,
    url_for,
)
from flask_login import current_user, login_required
from werkzeug.utils import secure_filename

from extensions import articles_collection
from models.models import Animal, Category, Pet, Product, Shelter, User, db
from services.product_service import add_category
from services.product_service import delete_category as do_delete_category
from services.product_service import delete_product as do_delete_product
from services.product_service import save_or_update_product, update_category
from services.shelter_service import (
    allowed_file,
    delete_animal,
    delete_pet,
    delete_shelter,
    save_or_update_animal,
    save_or_update_pet,
    save_or_update_shelter,
)

admin_bp = Blueprint("admin", __name__)


@admin_bp.after_request
def add_noindex_header(response):
    """Keep the back office out of search engine indexes."""
    response.headers["X-Robots-Tag"] = "noindex, nofollow"
    return response


def admin_required(view):
    """Restrict a view to authenticated users with the admin role."""

    @wraps(view)
    @login_required
    def wrapper(*args, **kwargs):
        if current_user.role != "admin":
            flash("Accès refusé.", "danger")
            return redirect(url_for("main.home"))
        return view(*args, **kwargs)

    return wrapper


# ============================
# Users
# ============================
@admin_bp.route("/edit-users", methods=["GET", "POST"])
@admin_required
def edit_users():
    page = request.args.get("page", 1, type=int)
    search_query = request.args.get("search", "")

    # Filter users by name, email, city or country
    users_query = User.query.filter(
        (User.first_name.ilike(f"%{search_query}%"))
        | (User.last_name.ilike(f"%{search_query}%"))
        | (User.email.ilike(f"%{search_query}%"))
        | (User.city.ilike(f"%{search_query}%"))
        | (User.country.ilike(f"%{search_query}%"))
    ).order_by(User.email)

    users = users_query.paginate(page=page, per_page=10, error_out=False)
    return render_template(
        "edit_users.html",
        users=users.items,
        total_pages=users.pages,
        prev_page=users.has_prev,
        next_page=users.has_next,
        current_page=page,
        search_query=search_query,
    )


@admin_bp.route("/edit-user/<int:user_id>", methods=["GET", "POST"])
@admin_required
def edit_user(user_id):
    user = User.query.get_or_404(user_id)
    if request.method == "POST":
        user.first_name = request.form.get("first_name")
        user.last_name = request.form.get("last_name")
        user.email = request.form.get("email")
        user.address_number = request.form.get("address_number")
        user.street_name = request.form.get("street_name")
        user.address_complement = request.form.get("address_complement")
        user.postal_code = request.form.get("postal_code")
        user.city = request.form.get("city")
        user.country = request.form.get("country")
        user.phone = request.form.get("phone")
        user.birth_date = request.form.get("birth_date")
        db.session.commit()
        return redirect(url_for("admin.edit_users"))
    return render_template("edit_user.html", user=user)


@admin_bp.route("/delete_user/<int:user_id>", methods=["POST"])
@admin_required
def delete_user(user_id):
    user = User.query.get_or_404(user_id)
    db.session.delete(user)
    db.session.commit()
    flash("Utilisateur supprimé avec succès.", "success")
    return redirect(url_for("admin.edit_users"))


# ============================
# Shelters & animals
# ============================
@admin_bp.route("/edit-shelters", methods=["GET", "POST"])
@admin_required
def edit_shelters():
    if request.method == "POST":
        file = request.files.get("image")
        if file and file.filename != "":
            if not allowed_file(file.filename):
                flash("Format d'image non autorisé.", "danger")
                return redirect(request.url)
            filename = secure_filename(file.filename)
            save_path = os.path.join(current_app.config["UPLOAD_FOLDER"], filename)
            try:
                file.save(save_path)
            except Exception as e:
                flash(
                    f"Erreur lors de l'enregistrement de l'image : {str(e)}", "danger"
                )
                return redirect(request.url)

    page = request.args.get("page", 1, type=int)
    search_query = request.args.get("search", "")
    per_page = 10

    # Filter shelters by name or address
    query = Shelter.query
    if search_query:
        query = query.filter(
            Shelter.name.ilike(f"%{search_query}%")
            | Shelter.address.ilike(f"%{search_query}%")
        )

    paginated = query.order_by(Shelter.name).paginate(
        page=page, per_page=per_page, error_out=False
    )

    return render_template(
        "edit_shelters.html",
        shelters=paginated.items,
        total_pages=paginated.pages,
        prev_page=paginated.has_prev,
        next_page=paginated.has_next,
        current_page=page,
        search_query=search_query,
    )


@admin_bp.route("/edit-shelter", methods=["GET", "POST"])
@admin_bp.route("/edit-shelter/<int:shelter_id>", methods=["GET", "POST"])
@admin_required
def edit_shelter(shelter_id=None):
    shelter = Shelter.query.get(shelter_id) if shelter_id else None

    if request.method == "POST":
        file = request.files.get("image")
        save_or_update_shelter(
            request.form, file, current_app.config["UPLOAD_FOLDER"], shelter
        )
        flash(
            "Refuge mis à jour avec succès." if shelter else "Nouveau refuge ajouté.",
            "success",
        )
        return redirect(url_for("admin.edit_shelters"))

    return render_template("edit_shelter.html", shelter=shelter)


@admin_bp.route("/delete_shelter/<int:shelter_id>", methods=["POST"])
@admin_required
def delete_shelter_route(shelter_id):
    delete_shelter(shelter_id)
    flash("Refuge supprimé avec succès.", "success")
    return redirect(url_for("admin.edit_shelters"))


@admin_bp.route("/edit_animals", methods=["GET"])
@admin_required
def edit_animals():
    page = request.args.get("page", 1, type=int)
    search_query = request.args.get("search", "")
    per_page = 10

    # Filter by species or breed if a search term is provided
    query = Animal.query
    if search_query:
        query = query.filter(
            Animal.species.ilike(f"%{search_query}%")
            | Animal.breed.ilike(f"%{search_query}%")
        )

    paginated = query.order_by(Animal.species, Animal.breed).paginate(
        page=page, per_page=per_page, error_out=False
    )

    return render_template(
        "edit_animals.html",
        animals=paginated.items,
        total_pages=paginated.pages,
        prev_page=paginated.has_prev,
        next_page=paginated.has_next,
        current_page=page,
        search_query=search_query,
    )


@admin_bp.route("/edit_animal", methods=["GET", "POST"])
@admin_bp.route("/edit_animal/<int:animal_id>", methods=["GET", "POST"])
@admin_required
def edit_animal(animal_id=None):
    animal = Animal.query.get_or_404(animal_id) if animal_id else None

    if request.method == "POST":
        save_or_update_animal(request.form, animal)
        flash("Animal mis à jour." if animal else "Nouvel animal ajouté.", "success")
        return redirect(url_for("admin.edit_animals"))

    return render_template("edit_animal.html", animal=animal)


@admin_bp.route("/delete_animal/<int:animal_id>", methods=["POST"])
@admin_required
def delete_animal_route(animal_id):
    delete_animal(animal_id)
    flash("Animal supprimé avec succès.", "success")
    return redirect(url_for("admin.edit_animals"))


@admin_bp.route("/edit_pets", methods=["GET"])
@admin_required
def edit_pets():
    page = request.args.get("page", 1, type=int)
    search_query = request.args.get("search", "")
    per_page = 10

    # Join Animal to allow filtering by species/breed as well as pet name
    query = Pet.query.join(Animal)
    if search_query:
        query = query.filter(
            Pet.name.ilike(f"%{search_query}%")
            | Animal.species.ilike(f"%{search_query}%")
            | Animal.breed.ilike(f"%{search_query}%")
        )

    paginated = query.order_by(Pet.name).paginate(
        page=page, per_page=per_page, error_out=False
    )

    shelters_list = Shelter.query.all()
    animals_list = Animal.query.all()

    return render_template(
        "edit_pets.html",
        pets=paginated.items,
        shelters=shelters_list,
        animals=animals_list,
        total_pages=paginated.pages,
        prev_page=paginated.has_prev,
        next_page=paginated.has_next,
        current_page=page,
        search_query=search_query,
    )


@admin_bp.route("/edit_pet", methods=["GET", "POST"])
@admin_bp.route("/edit_pet/<int:pet_id>", methods=["GET", "POST"])
@admin_required
def edit_pet(pet_id=None):
    pet = Pet.query.get_or_404(pet_id) if pet_id else None
    shelters_list = Shelter.query.all()
    animals_list = Animal.query.all()

    if request.method == "POST":
        save_or_update_pet(request.form, pet)
        flash(
            "Animal de compagnie mis à jour." if pet else "Nouvel animal ajouté.",
            "success",
        )
        return redirect(url_for("admin.edit_pets"))

    return render_template(
        "edit_pet.html", pet=pet, shelters=shelters_list, animals=animals_list
    )


@admin_bp.route("/delete_pet/<int:pet_id>", methods=["POST"])
@admin_required
def delete_pet_route(pet_id):
    delete_pet(pet_id)
    flash("Animal de compagnie supprimé avec succès.", "success")
    return redirect(url_for("admin.edit_pets"))


# ============================
# Products & categories
# ============================
@admin_bp.route("/edit_products", methods=["GET", "POST"])
@admin_required
def edit_products():
    page = request.args.get("page", 1, type=int)
    search_query = request.args.get("search", "")
    per_page = 10

    # Filter by product name or category name
    query = Product.query.outerjoin(Category)
    if search_query:
        query = query.filter(
            Product.name.ilike(f"%{search_query}%")
            | Category.name.ilike(f"%{search_query}%")
        )

    paginated = query.order_by(Product.name).paginate(
        page=page, per_page=per_page, error_out=False
    )

    categories = Category.query.all()

    return render_template(
        "edit_products.html",
        products=paginated.items,
        categories=categories,
        total_pages=paginated.pages,
        prev_page=paginated.has_prev,
        next_page=paginated.has_next,
        current_page=page,
        search_query=search_query,
    )


@admin_bp.route("/edit-product", methods=["POST"])
@admin_bp.route("/edit-product/<int:product_id>", methods=["GET", "POST"])
@admin_required
def edit_product(product_id=None):
    product = (
        Product.query.get_or_404(product_id) if product_id and product_id != 0 else None
    )
    categories = Category.query.all()

    if request.method == "POST":
        save_or_update_product(request.form, product)
        flash(
            "Produit mis à jour." if product else "Nouveau produit ajouté.", "success"
        )
        return redirect(url_for("admin.edit_products"))

    return render_template("edit_product.html", product=product, categories=categories)


@admin_bp.route("/delete_product/<int:product_id>", methods=["POST"])
@admin_required
def delete_product_route(product_id):
    do_delete_product(product_id)
    flash("Produit supprimé avec succès.", "success")
    return redirect(url_for("admin.edit_products"))


@admin_bp.route("/edit_categories", methods=["GET", "POST"])
@admin_required
def edit_categories():
    edit_id = request.args.get("edit", type=int)
    categories = Category.query.order_by(Category.name.asc()).all()

    for cat in categories:
        cat.editing = cat.category_id == edit_id

    return render_template("edit_categories.html", categories=categories)


@admin_bp.route("/add_category", methods=["POST"])
@admin_required
def add_category_route():
    add_category(request.form["name"])
    flash("Catégorie ajoutée avec succès.", "success")
    return redirect(url_for("admin.edit_categories"))


@admin_bp.route("/edit_category/<int:category_id>", methods=["POST"])
@admin_required
def edit_category(category_id):
    update_category(category_id, request.form["name"])
    flash("Catégorie mise à jour avec succès.", "success")
    return redirect(url_for("admin.edit_categories"))


@admin_bp.route("/delete_category/<int:category_id>", methods=["POST"])
@admin_required
def delete_category_route(category_id):
    do_delete_category(category_id)
    flash("Catégorie supprimée avec succès.", "success")
    return redirect(url_for("admin.edit_categories"))


# ============================
# Blog articles (MongoDB)
# ============================
@admin_bp.route("/edit-articles", methods=["GET", "POST"])
@admin_required
def edit_articles():
    page = int(request.args.get("page", 1))
    search_query = request.args.get("search", "")
    per_page = 10
    collection = articles_collection()

    if request.method == "POST":
        title = request.form["title"]
        content = request.form["content"]
        shelter_id = request.form.get("shelter_id") or None
        image = request.files["image"]
        image_filename = secure_filename(image.filename)
        image.save(os.path.join(current_app.config["UPLOAD_FOLDER"], image_filename))

        article = {
            "title": title,
            "content": content,
            "image_url": f"images/{image_filename}",
            "shelter_id": int(shelter_id) if shelter_id else None,
            "created_at": datetime.now(),
        }
        collection.insert_one(article)
        flash("Article créé avec succès.", "success")
        return redirect(url_for("admin.edit_articles"))

    # Build MongoDB filter based on search query (case-insensitive on title).
    # Escape the input so it is treated as a literal, not a user regex (ReDoS).
    mongo_filter = {}
    if search_query:
        mongo_filter = {"title": {"$regex": re.escape(search_query), "$options": "i"}}

    total_articles = collection.count_documents(mongo_filter)
    total_pages = (total_articles + per_page - 1) // per_page
    articles = list(
        collection.find(mongo_filter)
        .sort("created_at", -1)
        .skip((page - 1) * per_page)
        .limit(per_page)
    )
    shelters_list = Shelter.query.all()

    return render_template(
        "edit_articles.html",
        articles=articles,
        shelters=shelters_list,
        total_pages=total_pages,
        current_page=page,
        search_query=search_query,
    )


@admin_bp.route("/edit-article/<article_id>", methods=["GET", "POST"])
@admin_required
def edit_article(article_id):
    collection = articles_collection()
    article = collection.find_one({"_id": ObjectId(article_id)})

    if request.method == "POST":
        update_data = {
            "title": request.form["title"],
            "content": request.form["content"],
            "shelter_id": (
                int(request.form.get("shelter_id"))
                if request.form.get("shelter_id")
                else None
            ),
        }

        image = request.files.get("image")
        if image and image.filename != "":
            image_filename = secure_filename(image.filename)
            image.save(
                os.path.join(current_app.config["UPLOAD_FOLDER"], image_filename)
            )
            update_data["image_url"] = f"images/{image_filename}"

        collection.update_one({"_id": ObjectId(article_id)}, {"$set": update_data})
        flash("Article mis à jour.", "success")
        return redirect(url_for("admin.edit_articles"))

    shelters_list = Shelter.query.all()
    return render_template("edit_article.html", article=article, shelters=shelters_list)


@admin_bp.route("/delete-article/<article_id>", methods=["POST"])
@admin_required
def delete_article(article_id):
    articles_collection().delete_one({"_id": ObjectId(article_id)})
    flash("Article supprimé.", "success")
    return redirect(url_for("admin.edit_articles"))
