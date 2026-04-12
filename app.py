from flask import (
    Flask,
    render_template,
    request,
    redirect,
    url_for,
    flash,
    session,
    jsonify,
)

from services.cart_service import (
    get_cart,
    add_to_cart,
    update_cart,
    remove_from_cart,
    is_address_complete,
    get_cart_totals,
)

from flask_login import (
    LoginManager,
    login_user,
    logout_user,
    login_required,
    current_user,
)
from flask_migrate import Migrate
from flask_session import Session
from flask_mail import Mail, Message
from pymongo import MongoClient
from bson import ObjectId
from werkzeug.utils import secure_filename
from datetime import datetime
import os

from config import Config
from models.models import db, User, Product, Animal, Pet, Shelter, Category
from services.auth_service import (
    register_user,
    authenticate_user,
    generate_reset_token,
    verify_reset_token,
    reset_password as do_reset_password,
)
from services.cart_service import (
    get_cart,
    add_to_cart,
    update_cart,
    remove_from_cart,
    is_address_complete,
)
from services.shelter_service import (
    save_or_update_shelter,
    delete_shelter,
    save_or_update_animal,
    delete_animal,
    save_or_update_pet,
    delete_pet,
    allowed_file,
)
from services.product_service import (
    get_products_by_category,
    save_or_update_product,
    delete_product as do_delete_product,
    add_category,
    update_category,
    delete_category as do_delete_category,
)

from services.chat_service import send_message_to_make

 

# ============================
# App initialization
# ============================
app = Flask(__name__)
app.config.from_object(Config)

# ============================
# Extensions initialization
# ============================
db.init_app(app)
migrate = Migrate(app, db)
Session(app)
mail = Mail(app)

# ============================
# MongoDB connection
# ============================
client = MongoClient(app.config["MONGODB_URI"])
mongo_db = client.get_database()

# ============================
# Flask-Login setup
# ============================
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"


@login_manager.user_loader
def load_user(user_id):
    # Load user from database by ID for session management
    return User.query.get(int(user_id))


# ============================
# Routes - Public
# ============================
@app.route("/")
def home():
    return render_template("home.html")


# ============================
# Route - Chatbot
# ============================
@app.route("/chat", methods=["POST"])
def chat():
    data = request.get_json()
    user_message = data.get("message", "").strip()
    history = data.get("history", [])
 
    if not user_message:
        return jsonify({"success": False, "response": "Message vide."}), 400
 
    bot_response = send_message_to_make(user_message, history)
    return jsonify({"success": True, "response": bot_response})

@app.route("/glossary")
def glossary():
    letter = request.args.get("letter", "").upper()
    species = request.args.get("species", "").capitalize()

    query = Animal.query
    if letter and letter.isalpha():
        query = query.filter(Animal.breed.startswith(letter))
    if species:
        query = query.filter(Animal.species.ilike(species))

    animals_list = query.order_by(Animal.breed).all()
    return render_template(
        "glossary.html",
        animals=animals_list,
        selected_letter=letter,
        selected_species=species,
    )


@app.route("/glossary/<int:animal_id>")
def glossary_animal(animal_id):
    animal = Animal.query.get_or_404(animal_id)
    return render_template("glossary_animal.html", animal=animal)


@app.route("/shelters")
def shelters():
    shelters_data = Shelter.query.all()
    return render_template("shelters.html", shelters=shelters_data)


@app.route("/shelter/<int:shelter_id>")
def shelter(shelter_id):
    shelter_data = Shelter.query.get(shelter_id)
    if not shelter_data:
        return render_template("404.html")
    animals = Pet.query.filter_by(shelter_id=shelter_id).all()
    return render_template("shelter.html", shelter=shelter_data, animals=animals)


@app.route("/adopt-animals")
def adopt_animals():
    shelter_id = request.args.get("shelter_id", type=int)
    species = request.args.get("species", "").capitalize()

    query = Pet.query.join(Animal).filter(Pet.adoption_date.is_(None))
    if shelter_id:
        query = query.filter(Pet.shelter_id == shelter_id)
    if species:
        query = query.filter(Animal.species.ilike(species))

    pets = query.all()
    shelters_list = Shelter.query.all()
    selected_shelter = Shelter.query.get(shelter_id) if shelter_id else None
    animals = {pet.pet_id: Animal.query.get(pet.animal_id) for pet in pets}

    return render_template(
        "adopt_animals.html",
        pets=pets,
        animals=animals,
        shelters=shelters_list,
        selected_shelter=selected_shelter,
        selected_species=species,
    )


@app.route("/adopt-animal/<int:pet_id>")
def adopt_animal(pet_id):
    pet = Pet.query.get_or_404(pet_id)
    animal = Animal.query.get(pet.animal_id)
    return render_template("adopt_animal.html", pet=pet, animal=animal)


@app.route("/animals")
def animals():
    return render_template("animals.html")


@app.route("/products")
def products():
    category_name = request.args.get("category")
    products_list, categories = get_products_by_category(category_name)
    return render_template(
        "products.html",
        products=products_list,
        categories=categories,
        selected_category=category_name,
    )


@app.route("/product/<int:product_id>")
def product(product_id):
    product_item = Product.query.get_or_404(product_id)
    return render_template("product.html", product=product_item)


# ============================
# Routes - Blog
# ============================
@app.route("/blog")
def blog():
    collection = mongo_db.miaouff_collection
    page     = request.args.get("page", 1, type=int)
    per_page = 9

    total_articles = collection.count_documents({})
    total_pages    = (total_articles + per_page - 1) // per_page

    # Fetch articles for the current page, newest first
    articles = list(
        collection.find()
        .sort("created_at", -1)
        .skip((page - 1) * per_page)
        .limit(per_page)
    )

    return render_template(
        "blog.html",
        articles=articles,
        current_page=page,
        total_pages=total_pages,
    )


@app.route("/blog/<article_id>")
def blog_article(article_id):
    collection = mongo_db.miaouff_collection
    article    = collection.find_one({"_id": ObjectId(article_id)})

    # Return 404 if article doesn't exist
    if not article:
        return render_template(
            "error.html",
            error_code=404,
            error_title="Article introuvable",
            error_message="Cet article n'existe pas ou a été supprimé.",
        ), 404

    return render_template("blog_article.html", article=article)


@app.route("/contact")
def contact():
    return render_template("contact.html")


@app.route("/faq")
def faq():
    return render_template("faq.html")


@app.route("/privacy_policy")
def privacy_policy():
    return render_template("privacy_policy.html")


@app.route("/cookie_policy")
def cookie_policy():
    return render_template("cookie_policy.html")


@app.route("/legal_notices")
def legal_notices():
    return render_template("legal_notices.html")


@app.route("/terms_conditions")
def terms_conditions():
    return render_template("terms_conditions.html")


# ============================
# Routes - Games
# ============================
@app.route("/games")
def games():
    return render_template("games.html")


@app.route("/quiz")
def quiz():
    return render_template("quiz.html")


@app.route("/match")
def match():
    return render_template("match.html")


@app.route("/memory")
def memory():
    return render_template("memory.html")


@app.route("/wordsearch")
def wordsearch():
    return render_template("wordsearch.html")


@app.route("/hangman")
def hangman():
    return render_template("hangman.html")


@app.route("/rapido")
def rapido():
    return render_template("rapido.html")


# ============================
# Routes - Authentication
# ============================
@app.route("/login", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for("account"))

    if request.method == "POST":
        action = request.form.get("action")
        email = request.form.get("email")
        password = request.form.get("password")

        if action == "register":
            success, message = register_user(email, password)
            flash(message, "success" if success else "danger")
            return redirect(url_for("login"))

        elif action == "login":
            user = authenticate_user(email, password)
            if user:
                login_user(user)
                next_page = request.args.get("next")
                return redirect(next_page or url_for("account"))
            flash("Identifiants incorrects.", "danger")
            return redirect(url_for("login"))

    return render_template("login.html")


@app.route("/account")
@login_required
def account():
    return render_template("account.html", user_name=current_user.email)


@app.route("/logout")
@login_required
def logout():
    logout_user()
    flash("Vous êtes déconnecté.", "success")
    return redirect(url_for("login"))


@app.route("/send_reset_code/<int:user_id>")
def send_reset_code(user_id):
    user = User.query.get(user_id)
    if not user:
        flash("Utilisateur introuvable.", "danger")
        return redirect(url_for("edit_users"))

    reset_code = generate_reset_token(user.email)
    msg = Message("Réinitialisation de votre mot de passe", recipients=[user.email])
    msg.html = f"""
    <html>
        <body>
            <h2 style="color: #4CAF50;">Réinitialisation de votre mot de passe</h2>
            <p>Bonjour {user.first_name} {user.last_name},</p>
            <p>Veuillez utiliser le code suivant pour réinitialiser votre mot de passe :</p>
            <h3 style="background-color: #f4f4f4; padding: 10px; border-radius: 5px; color: #333;">
                {reset_code}
            </h3>
            <p>Si vous n'avez pas demandé cette réinitialisation, ignorez cet e-mail.</p>
            <p>Cordialement,<br>L'équipe Miaouff</p>
        </body>
    </html>
    """
    try:
        mail.send(msg)
        flash("Le code a été envoyé par mail.", "success")
    except Exception as e:
        flash(f"Erreur lors de l'envoi du mail : {str(e)}", "danger")

    return redirect(url_for("edit_users"))


@app.route("/reset_password", methods=["GET", "POST"])
def reset_password():
    if request.method == "POST":
        email = request.form.get("email")
        code = request.form.get("code")
        new_password = request.form.get("new_password")

        if not verify_reset_token(email, code):
            flash("Code invalide.", "danger")
            return redirect(url_for("reset_password"))

        success, message = do_reset_password(email, new_password)
        flash(message, "success" if success else "danger")
        if success:
            return redirect(url_for("login"))

    return render_template("reset_password.html")


# ============================
# Routes - Cart & Orders
# ============================
@app.route("/cart")
def cart():
    cart_items = get_cart(session)
    totals = get_cart_totals(cart_items)
    return render_template("cart.html", cart=cart_items, totals=totals)


@app.route("/add_to_cart/<int:product_id>", methods=["POST"])
def add_to_cart_route(product_id):
    data = request.get_json()
    quantity_requested = int(data.get("quantity", 1))
    success, message = add_to_cart(session, product_id, quantity_requested)
    if not success:
        return jsonify({"success": False, "message": message}), 400
    return jsonify({"success": True})


@app.route("/update_cart/<int:product_id>", methods=["POST"])
def update_cart_route(product_id):
    data = request.get_json()
    new_quantity = int(data.get("quantity", 1))
    success, message, corrected = update_cart(session, product_id, new_quantity)
    if not success:
        return jsonify({"success": False, "message": message, "corrected_quantity": corrected}), 400
    return jsonify({"success": True})


@app.route("/remove_from_cart/<int:product_id>", methods=["POST"])
def remove_from_cart_route(product_id):
    remove_from_cart(session, product_id)
    return redirect(url_for("cart"))


@app.route("/check_order")
@login_required
def check_order():
    """
    Entry point for the checkout flow.
    Redirects to address edit if address is incomplete, otherwise shows the order summary.
    """
    user = User.query.get(current_user.user_id)
    cart_items = get_cart(session)

    if not cart_items:
        flash("Votre panier est vide.", "danger")
        return redirect(url_for("cart"))

    if not is_address_complete(user):
        flash("Veuillez compléter votre adresse de livraison.", "danger")
        return redirect(url_for("edit_address"))

    totals = get_cart_totals(cart_items)
    return render_template("check_order.html", cart=cart_items, user=user, totals=totals)


@app.route("/payment", methods=["GET", "POST"])
@login_required
def payment():
    """
    Show the Stripe payment page.
    On POST: create a Stripe PaymentIntent and return the client secret.
    """
    import stripe
    stripe.api_key = app.config["STRIPE_SECRET_KEY"]

    cart_items = get_cart(session)
    if not cart_items:
        return redirect(url_for("cart"))

    totals = get_cart_totals(cart_items)

    if request.method == "POST":
        # Amount in cents for Stripe
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
        stripe_public_key=app.config["STRIPE_PUBLIC_KEY"],
    )


@app.route("/payment_success", methods=["POST"])
@login_required
def payment_success():
    """
    Called by the frontend after Stripe confirms payment.
    Creates the Order and OrderProduct records, clears the cart.
    """
    from models.models import Order, OrderProduct, Payment as PaymentModel
    from datetime import datetime

    cart_items = get_cart(session)
    if not cart_items:
        return jsonify({"success": False}), 400

    totals = get_cart_totals(cart_items)
    user = User.query.get(current_user.user_id)

    # Create the order
    order = Order(
        user_id=user.user_id,
        order_date=datetime.now(),
        status="paid",
        total_price_excl_tax=totals["total_excl_tax"],
        total_price_incl_tax=totals["total_incl_tax"],
        shipping_fee=totals["shipping_fee"],
    )
    db.session.add(order)
    db.session.flush()  # Get order_id before committing

    # Create order lines and update stock
    for item in cart_items:
        product = Product.query.get(item["product_id"])
        if product:
            op = OrderProduct(
                order_id=order.order_id,
                product_id=item["product_id"],
                quantity=item["quantity"],
                unit_price_excl_tax=round(item["price"] / 1.20, 2),
                unit_price_incl_tax=item["price"],
            )
            db.session.add(op)
            # Decrement stock
            product.stock = max(0, product.stock - item["quantity"])

    # Create payment record
    data = request.get_json()
    payment = PaymentModel(
        payment_method="card",
        payment_status="paid",
        payment_date=datetime.now(),
        payment_total=totals["grand_total"],
        order_id=order.order_id,
    )
    db.session.add(payment)
    db.session.commit()

    # Clear the cart
    session["cart"] = []
    session.modified = True

    return jsonify({"success": True, "order_id": order.order_id})


@app.route("/order_confirmation/<int:order_id>")
@login_required
def order_confirmation(order_id):
    """Show the order confirmation page after successful payment."""
    from models.models import Order
    order = Order.query.get_or_404(order_id)
    # Security: only the order owner can see their confirmation
    if order.user_id != current_user.user_id:
        return redirect(url_for("home"))
    return render_template("order_confirmation.html", order=order)


@app.route("/edit_address", methods=["GET", "POST"])
@login_required
def edit_address():
    """Let the user fill in their delivery address."""
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
        return redirect(url_for("check_order"))

    return render_template("edit_address.html", user=user)


# ============================
# Routes - Admin users
# ============================
@app.route("/edit-users", methods=["GET", "POST"])
def edit_users():
    page = request.args.get("page", 1, type=int)
    search_query = request.args.get("search", "")

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


@app.route("/edit-user/<int:user_id>", methods=["GET", "POST"])
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
        return redirect(url_for("edit_users"))
    return render_template("edit_user.html", user=user)


@app.route("/delete_user/<int:user_id>", methods=["POST"])
@login_required
def delete_user(user_id):
    user = User.query.get_or_404(user_id)
    db.session.delete(user)
    db.session.commit()
    flash("Utilisateur supprimé avec succès.", "success")
    return redirect(url_for("edit_users"))


# ============================
# Routes - Admin shelters & animals
# ============================
@app.route("/edit-shelters", methods=["GET", "POST"])
@login_required
def edit_shelters():
    if current_user.role != "admin":
        flash("Accès refusé.", "danger")
        return redirect(url_for("home"))

    if request.method == "POST":
        file = request.files.get("image")
        if file and file.filename != "":
            if not allowed_file(file.filename):
                flash("Format d'image non autorisé.", "danger")
                return redirect(request.url)
            filename = secure_filename(file.filename)
            save_path = os.path.join(app.config["UPLOAD_FOLDER"], filename)
            try:
                file.save(save_path)
            except Exception as e:
                flash(f"Erreur lors de l'enregistrement de l'image : {str(e)}", "danger")
                return redirect(request.url)

    shelters_list = Shelter.query.all()
    return render_template("edit_shelters.html", shelters=shelters_list)


@app.route("/edit-shelter", methods=["GET", "POST"])
@app.route("/edit-shelter/<int:shelter_id>", methods=["GET", "POST"])
@login_required
def edit_shelter(shelter_id=None):
    if current_user.role != "admin":
        flash("Accès refusé.", "danger")
        return redirect(url_for("home"))

    shelter = Shelter.query.get(shelter_id) if shelter_id else None

    if request.method == "POST":
        file = request.files.get("image")
        save_or_update_shelter(request.form, file, app.config["UPLOAD_FOLDER"], shelter)
        flash("Refuge mis à jour avec succès." if shelter else "Nouveau refuge ajouté.", "success")
        return redirect(url_for("edit_shelters"))

    return render_template("edit_shelter.html", shelter=shelter)


@app.route("/delete_shelter/<int:shelter_id>", methods=["POST"])
@login_required
def delete_shelter_route(shelter_id):
    if current_user.role != "admin":
        flash("Accès refusé.", "danger")
        return redirect(url_for("edit_shelters"))
    delete_shelter(shelter_id)
    flash("Refuge supprimé avec succès.", "success")
    return redirect(url_for("edit_shelters"))


@app.route("/edit_animals", methods=["GET"])
@login_required
def edit_animals():
    if current_user.role != "admin":
        flash("Accès refusé.", "danger")
        return redirect(url_for("home"))
    animals_list = Animal.query.all()
    return render_template("edit_animals.html", animals=animals_list)


@app.route("/edit_animal", methods=["GET", "POST"])
@app.route("/edit_animal/<int:animal_id>", methods=["GET", "POST"])
@login_required
def edit_animal(animal_id=None):
    if current_user.role != "admin":
        flash("Accès refusé.", "danger")
        return redirect(url_for("home"))

    animal = Animal.query.get_or_404(animal_id) if animal_id else None

    if request.method == "POST":
        save_or_update_animal(request.form, animal)
        flash("Animal mis à jour." if animal else "Nouvel animal ajouté.", "success")
        return redirect(url_for("edit_animals"))

    return render_template("edit_animal.html", animal=animal)


@app.route("/delete_animal/<int:animal_id>", methods=["POST"])
@login_required
def delete_animal_route(animal_id):
    if current_user.role != "admin":
        flash("Accès refusé.", "danger")
        return redirect(url_for("home"))
    delete_animal(animal_id)
    flash("Animal supprimé avec succès.", "success")
    return redirect(url_for("edit_animals"))


@app.route("/edit_pets", methods=["GET"])
@login_required
def edit_pets():
    if current_user.role != "admin":
        flash("Accès refusé.", "danger")
        return redirect(url_for("home"))
    pets = Pet.query.all()
    return render_template("edit_pets.html", pets=pets)


@app.route("/edit_pet", methods=["GET", "POST"])
@app.route("/edit_pet/<int:pet_id>", methods=["GET", "POST"])
@login_required
def edit_pet(pet_id=None):
    if current_user.role != "admin":
        flash("Accès refusé.", "danger")
        return redirect(url_for("home"))

    pet = Pet.query.get_or_404(pet_id) if pet_id else None
    shelters_list = Shelter.query.all()
    animals_list = Animal.query.all()

    if request.method == "POST":
        save_or_update_pet(request.form, pet)
        flash("Animal de compagnie mis à jour." if pet else "Nouvel animal ajouté.", "success")
        return redirect(url_for("edit_pets"))

    return render_template("edit_pet.html", pet=pet, shelters=shelters_list, animals=animals_list)


@app.route("/delete_pet/<int:pet_id>", methods=["POST"])
@login_required
def delete_pet_route(pet_id):
    if current_user.role != "admin":
        flash("Accès refusé.", "danger")
        return redirect(url_for("home"))
    delete_pet(pet_id)
    flash("Animal de compagnie supprimé avec succès.", "success")
    return redirect(url_for("edit_pets"))


# ============================
# Routes - Admin products & categories
# ============================
@app.route("/edit_products", methods=["GET", "POST"])
@login_required
def edit_products():
    if current_user.role != "admin":
        flash("Accès refusé.", "danger")
        return redirect(url_for("home"))
    products_list = Product.query.all()
    categories = Category.query.all()
    return render_template("edit_products.html", products=products_list, categories=categories)


@app.route("/edit-product", methods=["POST"])
@app.route("/edit-product/<int:product_id>", methods=["GET", "POST"])
@login_required
def edit_product(product_id=None):
    if current_user.role != "admin":
        flash("Accès refusé.", "danger")
        return redirect(url_for("home"))

    product = Product.query.get_or_404(product_id) if product_id and product_id != 0 else None
    categories = Category.query.all()

    if request.method == "POST":
        save_or_update_product(request.form, product)
        flash("Produit mis à jour." if product else "Nouveau produit ajouté.", "success")
        return redirect(url_for("edit_products"))

    return render_template("edit_product.html", product=product, categories=categories)


@app.route("/delete_product/<int:product_id>", methods=["POST"])
@login_required
def delete_product_route(product_id):
    if current_user.role != "admin":
        flash("Accès refusé.", "danger")
        return redirect(url_for("home"))
    do_delete_product(product_id)
    flash("Produit supprimé avec succès.", "success")
    return redirect(url_for("edit_products"))


@app.route("/edit_categories", methods=["GET", "POST"])
@login_required
def edit_categories():
    if current_user.role != "admin":
        flash("Accès refusé.", "danger")
        return redirect(url_for("home"))

    edit_id = request.args.get("edit", type=int)
    categories = Category.query.order_by(Category.name.asc()).all()

    # Flag the category currently being edited
    for cat in categories:
        cat.editing = cat.category_id == edit_id

    return render_template("edit_categories.html", categories=categories)


@app.route("/add_category", methods=["POST"])
@login_required
def add_category_route():
    if current_user.role != "admin":
        flash("Accès refusé.", "danger")
        return redirect(url_for("home"))
    add_category(request.form["name"])
    flash("Catégorie ajoutée avec succès.", "success")
    return redirect(url_for("edit_categories"))


@app.route("/edit_category/<int:category_id>", methods=["POST"])
@login_required
def edit_category(category_id):
    if current_user.role != "admin":
        flash("Accès refusé.", "danger")
        return redirect(url_for("home"))
    update_category(category_id, request.form["name"])
    flash("Catégorie mise à jour avec succès.", "success")
    return redirect(url_for("edit_categories"))


@app.route("/delete_category/<int:category_id>", methods=["POST"])
@login_required
def delete_category_route(category_id):
    if current_user.role != "admin":
        flash("Accès refusé.", "danger")
        return redirect(url_for("home"))
    do_delete_category(category_id)
    flash("Catégorie supprimée avec succès.", "success")
    return redirect(url_for("edit_categories"))


# ============================
# Routes - Admin articles (MongoDB)
# ============================
@app.route("/edit-articles", methods=["GET", "POST"])
@login_required
def edit_articles():
    if current_user.role != "admin":
        flash("Accès refusé.", "danger")
        return redirect(url_for("home"))

    page = int(request.args.get("page", 1))
    per_page = 10
    collection = mongo_db.miaouff_collection

    if request.method == "POST":
        title = request.form["title"]
        content = request.form["content"]
        shelter_id = request.form.get("shelter_id") or None
        image = request.files["image"]
        image_filename = secure_filename(image.filename)
        image.save(os.path.join(app.config["UPLOAD_FOLDER"], image_filename))

        article = {
            "title": title,
            "content": content,
            "image_url": f"images/{image_filename}",
            "shelter_id": int(shelter_id) if shelter_id else None,
            "created_at": datetime.now(),
        }
        collection.insert_one(article)
        flash("Article créé avec succès.", "success")
        return redirect(url_for("edit_articles"))

    total_articles = collection.count_documents({})
    total_pages = (total_articles + per_page - 1) // per_page
    articles = list(
        collection.find()
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
    )


@app.route("/edit-article/<article_id>", methods=["GET", "POST"])
@login_required
def edit_article(article_id):
    if current_user.role != "admin":
        flash("Accès refusé.", "danger")
        return redirect(url_for("home"))

    collection = mongo_db.miaouff_collection
    article = collection.find_one({"_id": ObjectId(article_id)})

    if request.method == "POST":
        update_data = {
            "title": request.form["title"],
            "content": request.form["content"],
            "shelter_id": int(request.form.get("shelter_id")) if request.form.get("shelter_id") else None,
        }

        # Only update image if a new one was uploaded
        image = request.files.get("image")
        if image and image.filename != "":
            image_filename = secure_filename(image.filename)
            image.save(os.path.join(app.config["UPLOAD_FOLDER"], image_filename))
            update_data["image_url"] = f"images/{image_filename}"

        collection.update_one({"_id": ObjectId(article_id)}, {"$set": update_data})
        flash("Article mis à jour.", "success")
        return redirect(url_for("edit_articles"))

    shelters_list = Shelter.query.all()
    return render_template("edit_article.html", article=article, shelters=shelters_list)


@app.route("/delete-article/<article_id>", methods=["POST"])
@login_required
def delete_article(article_id):
    if current_user.role != "admin":
        flash("Accès refusé.", "danger")
        return redirect(url_for("home"))
    mongo_db.miaouff_collection.delete_one({"_id": ObjectId(article_id)})
    flash("Article supprimé.", "success")
    return redirect(url_for("edit_articles"))


# ============================
# Error handlers
# ============================
# One unified template handles all HTTP errors.
# Each handler passes a code, a short title and a human-friendly message.

def render_error(code, title, message):
    """Helper to render the shared error template with the right HTTP status."""
    return render_template(
        "error.html",
        error_code=code,
        error_title=title,
        error_message=message,
    ), code


@app.errorhandler(401)
def error_401(_):
    # Triggered when authentication is required but not provided
    return render_error(
        401,
        "Accès refusé",
        "Vous devez être connecté pour accéder à cette page. 🔐",
    )


@app.errorhandler(403)
def error_403(_):
    # Triggered when the user is authenticated but not authorised
    return render_error(
        403,
        "Permission refusée",
        "Vous n'avez pas les droits nécessaires pour accéder à cette ressource.",
    )


@app.errorhandler(404)
def error_404(_):
    # Page not found — the most common error
    return render_error(
        404,
        "Page introuvable",
        "Oups ! On a cherché partout... même sous le canapé 🐾\nCette page n'existe pas (ou plus).",
    )


@app.errorhandler(429)
def error_429(_):
    # Too many requests — rate limiting
    return render_error(
        429,
        "Trop de requêtes",
        "Vous avez effectué trop de tentatives en peu de temps. Patientez un instant avant de réessayer.",
    )


@app.errorhandler(500)
def error_500(_):
    # Internal server error — unexpected crash
    return render_error(
        500,
        "Erreur serveur",
        "Une erreur inattendue s'est produite de notre côté. Notre équipe a été notifiée. 🛠️",
    )


@app.errorhandler(503)
def error_503(_):
    # Service unavailable — maintenance or overload
    return render_error(
        503,
        "Service indisponible",
        "Le site est temporairement indisponible pour maintenance. Revenez dans quelques minutes.",
    )


# ============================
# Entry point
# ============================
if __name__ == '__main__':
    # debug=True is for local development only, never use in production
    app.run(debug=os.environ.get('FLASK_DEBUG', 'False') == 'True')