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
from flask_login import (
    LoginManager,
    login_user,
    logout_user,
    login_required,
    current_user,
)
from setup_db import (
    db,
    User,
    Product,
    Order,
    OrderProduct,
    Category,
    Payment,
    Shelter,
    Animal,
    Pet,
)
import psycopg2
from dotenv import load_dotenv
from pymongo import MongoClient
import os
from flask_session import Session
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename
from flask_mail import Mail, Message
import secrets
from bson import ObjectId
from datetime import datetime
import re

app = Flask(__name__)

app.config["SESSION_TYPE"] = "filesystem"
app.config["SECRET_KEY"] = os.getenv("SECRET_KEY")
Session(app)

mongo_uri = os.getenv("MONGODB_URI")
client = MongoClient(mongo_uri)
mongo_db = client.get_database()

load_dotenv()
app.secret_key = os.getenv("SECRET_KEY")
app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("DATABASE_URL")
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

app.config["MAIL_SERVER"] = os.getenv("MAIL_SERVER")
app.config["MAIL_PORT"] = int(os.getenv("MAIL_PORT"))
app.config["MAIL_USE_TLS"] = os.getenv("MAIL_USE_TLS") == "True"
app.config["MAIL_USERNAME"] = os.getenv("MAIL_USERNAME")
app.config["MAIL_PASSWORD"] = os.getenv("MAIL_PASSWORD")
app.config["MAIL_DEFAULT_SENDER"] = os.getenv("MAIL_DEFAULT_SENDER")

mail = Mail(app)

BASE_DIR = os.path.abspath(os.path.dirname(__file__))
UPLOAD_FOLDER = os.path.join(BASE_DIR, "static", "images")
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER
ALLOWED_EXTENSIONS = {"png", "jpg", "jpeg", "gif"}


def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS


db.init_app(app)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


def get_id(self):
    return str(self.user_id)


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


@app.route("/")
def home():
    return render_template("home.html")


reset_tokens = {}


@app.route("/send_reset_code/<int:user_id>")
def send_reset_code(user_id):
    user = User.query.get(user_id)
    if not user:
        flash("Utilisateur introuvable.", "danger")
        return redirect(url_for("edit_users"))

    reset_code = secrets.token_hex(4)
    reset_tokens[user.email] = reset_code

    msg = Message("Réinitialisation de votre mot de passe", recipients=[user.email])

    msg.html = f"""
    <html>
        <body>
            <h2 style="color: #4CAF50;">Réinitialisation de votre mot de passe</h2>
            <p>Bonjour {user.first_name} {user.last_name},</p>
            <p>Nous avons reçu une demande de réinitialisation de votre mot de passe. 
            Veuillez utiliser le code suivant pour réinitialiser votre mot de passe :</p>
            <h3 style="background-color: #f4f4f4; padding: 10px; border-radius: 5px; color: #333;">
                {reset_code}
            </h3>
            <p>Si vous n'avez pas demandé cette réinitialisation, veuillez ignorer cet e-mail.</p>
            <p>Cordialement,<br>
            L'équipe Miaouff</p>
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

        if reset_tokens.get(email) != code:
            flash("Code invalide.", "danger")
            return redirect(url_for("reset_password"))

        user = User.query.filter_by(email=email).first()
        if user:
            user.password = generate_password_hash(new_password, method="pbkdf2:sha256")
            db.session.commit()
            flash("Mot de passe modifié avec succès !", "success")
            reset_tokens.pop(email, None)
            return redirect(url_for("login"))

    return render_template("reset_password.html")


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

    total_pages = users.pages
    prev_page = users.has_prev
    next_page = users.has_next

    return render_template(
        "edit_users.html",
        users=users.items,
        total_pages=total_pages,
        prev_page=prev_page,
        next_page=next_page,
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

# Login and register
@app.route("/login", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for("account"))

    if request.method == "POST":
        action = request.form.get("action")
        email = request.form.get("email")
        password = request.form.get("password")

        if action == "register":
            confirm_password = request.form.get("confirm_password")

            if User.query.filter_by(email=email).first():
                flash("Cet e-mail est déjà utilisé.", "danger")
                return redirect(url_for("login"))

            if password != confirm_password:
                flash("Les mots de passe ne correspondent pas.", "danger")
                return redirect(url_for("login"))

            if (
            len(password) < 12
            or not any(c.isupper() for c in password)
            or not any(c.islower() for c in password)
            or not any(c.isdigit() for c in password)
            or not re.search(r'[@$!%*?&,.;:\-_+=()\[\]{}\/\\|^~#]', password)
        ):
                flash("Le mot de passe ne respecte pas les critères de sécurité.", "danger")
                return redirect(url_for("login"))


            hashed_password = generate_password_hash(password, method="pbkdf2:sha256")
            new_user = User(email=email, password=hashed_password, role="user")
            db.session.add(new_user)
            db.session.commit()
            flash(
                "Inscription réussie ! Vous pouvez maintenant vous connecter.",
                "success",
            )
            return redirect(url_for("login"))

        elif action == "login":
            user = User.query.filter_by(email=email).first()
            if user and check_password_hash(user.password, password):
                login_user(user)

                next_page = request.args.get("next")
                return redirect(next_page or url_for("account"))
            else:
                flash("Identifiants incorrects.", "danger")
                return redirect(url_for("login"))

    return render_template("login.html")

# To log to the account
@app.route("/account")
@login_required
def account():
    return render_template("account.html", user_name=current_user.email)

# To logout
@app.route("/logout")
@login_required
def logout():
    logout_user()
    flash("Vous êtes déconnecté.", "success")
    return redirect(url_for("login"))


@app.route("/edit-shelters", methods=["GET", "POST"])
@login_required
def edit_shelters():
    if current_user.role != "admin":
        flash("Accès refusé.", "danger")
        return redirect(url_for("index"))

    shelters = Shelter.query.all()

    if request.method == "POST":

        shelter_id_to_delete = request.form.get("shelter_id")
        if shelter_id_to_delete:
            shelter = Shelter.query.get(int(shelter_id_to_delete))
            if shelter:
                if shelter.image:
                    image_path = os.path.join(app.config["UPLOAD_FOLDER"], shelter.image)
                    if os.path.exists(image_path):
                        os.remove(image_path)
                db.session.delete(shelter)
                db.session.commit()
                flash("Refuge supprimé avec succès", "success")
            return redirect(url_for("edit_shelters"))


        name = request.form.get("name")
        address = request.form.get("address")
        phone = request.form.get("phone")
        email = request.form.get("email")
        description = request.form.get("description")
        image_file = request.files.get("image")  

        if not image_file:
            flash("Veuillez sélectionner une image", "danger")
            return redirect(url_for("edit_shelters"))


        filename = secure_filename(image_file.filename)
        image_path = os.path.join(app.config["UPLOAD_FOLDER"], filename)
        image_file.save(image_path)

        new_shelter = Shelter(
            name=name,
            address=address,
            phone=phone,
            email=email,
            description=description,
            image=filename
        )
        db.session.add(new_shelter)
        db.session.commit()
        flash("Refuge ajouté avec succès", "success")
        return redirect(url_for("edit_shelters"))

    return render_template("edit_shelters.html", shelters=shelters)



@app.route("/edit-shelter", methods=["GET", "POST"])
@app.route("/edit-shelter/<int:shelter_id>", methods=["GET", "POST"])
@login_required
def edit_shelter(shelter_id=None):
    if current_user.role != "admin":
        flash("Accès refusé.", "danger")
        return redirect(url_for("home"))

    shelter = Shelter.query.get(shelter_id) if shelter_id else None
    all_shelters = Shelter.query.all()  # Pour un select si nécessaire
    all_species = [s[0] for s in db.session.query(Animal.species).distinct().all()]  # Toutes espèces

    if request.method == "POST":
        name = request.form["name"]
        address = request.form["address"]
        phone = request.form["phone"]
        email = request.form["email"]
        description = request.form.get("description", "")

        file = request.files.get("image")
        image_filename = shelter.image if shelter else None

        if file and file.filename != "":
            if allowed_file(file.filename):
                filename = secure_filename(file.filename)
                filepath = os.path.join(app.config["UPLOAD_FOLDER"], filename)

                # Supprime ancienne image si existante
                if shelter and shelter.image:
                    old_image_path = os.path.join(app.config["UPLOAD_FOLDER"], shelter.image)
                    if os.path.exists(old_image_path):
                        os.remove(old_image_path)

                file.save(filepath)
                image_filename = filename
            else:
                flash("Format d'image non autorisé.", "danger")
                return redirect(request.url)

        if shelter:
            shelter.name = name
            shelter.address = address
            shelter.phone = phone
            shelter.email = email
            shelter.description = description
            shelter.image = image_filename
            flash("Refuge mis à jour avec succès", "success")
        else:
            shelter = Shelter(
                name=name,
                address=address,
                phone=phone,
                email=email,
                description=description,
                image=image_filename,
            )
            db.session.add(shelter)
            flash("Nouveau refuge ajouté avec succès", "success")

        db.session.commit()
        return redirect(url_for("edit_shelters"))

    return render_template(
        "edit_shelter.html",
        shelter=shelter,
        all_shelters=all_shelters,
        all_species=all_species
    )


@app.route("/delete_shelter/<int:shelter_id>", methods=["POST"])
@login_required
def delete_shelter(shelter_id):
    if current_user.role != "admin":
        flash("Accès refusé.", "danger")
        return redirect(url_for("edit_shelters"))

    shelter = Shelter.query.get_or_404(shelter_id)

    db.session.delete(shelter)
    db.session.commit()
    flash("Refuge supprimé avec succès", "success")

    return redirect(url_for("edit_shelters"))


@app.route("/edit_animals", methods=["GET"])
@login_required
def edit_animals():
    if current_user.role != "admin":
        flash("Accès refusé.", "danger")
        return redirect(url_for("home"))

    animals = Animal.query.all()
    return render_template("edit_animals.html", animals=animals)


@app.route("/edit_animal", methods=["GET", "POST"])
@app.route("/edit_animal/<int:animal_id>", methods=["GET", "POST"])
@login_required
def edit_animal(animal_id=None):
    if current_user.role != "admin":
        flash("Accès refusé.", "danger")
        return redirect(url_for("home"))

    animal = None
    if animal_id:
        animal = Animal.query.get_or_404(animal_id)

    if request.method == "POST":
        species = request.form["species"]
        breed = request.form["breed"]
        lifespan = request.form.get("lifespan", "")
        diet = request.form.get("diet", "")
        specifics = request.form.get("specifics", "")
        image = request.form.get("image", "")

        if animal:
            animal.species = species
            animal.breed = breed
            animal.lifespan = lifespan
            animal.diet = diet
            animal.specifics = specifics
            animal.image = image
            flash("Animal mis à jour avec succès", "success")
        else:
            animal = Animal(
                species=species,
                breed=breed,
                lifespan=lifespan,
                diet=diet,
                specifics=specifics,
                image=image,
            )
            db.session.add(animal)
            flash("Nouvel animal ajouté avec succès", "success")

        db.session.commit()
        return redirect(url_for("edit_animals"))

    return render_template("edit_animal.html", animal=animal)


@app.route("/delete_animal/<int:animal_id>", methods=["POST"])
@login_required
def delete_animal(animal_id):
    if current_user.role != "admin":
        flash("Accès refusé.", "danger")
        return redirect(url_for("home"))

    animal = Animal.query.get_or_404(animal_id)
    db.session.delete(animal)
    db.session.commit()
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

    pet = None
    shelters = Shelter.query.all()
    animals = Animal.query.all()

    if pet_id:
        pet = Pet.query.get_or_404(pet_id)

    if request.method == "POST":
        name = request.form["name"]
        age = int(request.form["age"])
        gender = request.form["gender"]
        description = request.form.get("description", "")
        adoption_date = request.form.get("adoption_date", None)
        image = request.form.get("image", "")
        shelter_id = int(request.form["shelter_id"])
        animal_id = int(request.form["animal_id"])

        if pet:
            pet.name = name
            pet.age = age
            pet.gender = gender
            pet.description = description
            pet.adoption_date = adoption_date
            pet.image = image
            pet.shelter_id = shelter_id
            pet.animal_id = animal_id
            flash("Animal de compagnie mis à jour avec succès.", "success")
        else:
            pet = Pet(
                name=name,
                age=age,
                gender=gender,
                description=description,
                adoption_date=adoption_date,
                image=image,
                shelter_id=shelter_id,
                animal_id=animal_id,
            )
            db.session.add(pet)
            flash("Nouvel animal de compagnie ajouté avec succès.", "success")

        db.session.commit()
        return redirect(url_for("edit_pets"))

    return render_template("edit_pet.html", pet=pet, shelters=shelters, animals=animals)


@app.route("/delete_pet/<int:pet_id>", methods=["POST"])
@login_required
def delete_pet(pet_id):
    if current_user.role != "admin":
        flash("Accès refusé.", "danger")
        return redirect(url_for("home"))

    pet = Pet.query.get_or_404(pet_id)
    db.session.delete(pet)
    db.session.commit()
    flash("Animal de compagnie supprimé avec succès.", "success")

    return redirect(url_for("edit_pets"))


@app.route("/edit_products", methods=["GET", "POST"])
@login_required
def edit_products():
    if current_user.role != "admin":
        flash("Accès refusé.", "danger")
        return redirect(url_for("home"))

    products = Product.query.all()
    categories = Category.query.all()
    return render_template(
        "edit_products.html", products=products, categories=categories
    )


@app.route("/edit-product", methods=["POST"])
@app.route("/edit-product/<int:product_id>", methods=["GET", "POST"])
@login_required
def edit_product(product_id=None):
    if current_user.role != "admin":
        flash("Accès refusé.", "danger")
        return redirect(url_for("home"))

    product = None
    categories = Category.query.all()

    if product_id and product_id != 0:
        product = Product.query.get_or_404(product_id)

    if request.method == "POST":
        name = request.form["name"]
        description = request.form.get("description", "")
        price_excl_tax = request.form["price_excl_tax"]
        price_incl_tax = request.form["price_incl_tax"]
        stock = request.form["stock"]
        weight = request.form["weight"]
        image = request.form.get("image", "")
        category_id = request.form.get("category_id")

        if product:
            product.name = name
            product.description = description
            product.price_excl_tax = price_excl_tax
            product.price_incl_tax = price_incl_tax
            product.stock = stock
            product.weight = weight
            product.image = image
            product.category_id = category_id
            flash("Produit mis à jour avec succès.", "success")
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
            flash("Nouveau produit ajouté avec succès.", "success")

        db.session.commit()
        return redirect(url_for("edit_products"))

    return render_template("edit_product.html", product=product, categories=categories)


@app.route("/delete_product/<int:product_id>", methods=["POST"])
@login_required
def delete_product(product_id):
    if current_user.role != "admin":
        flash("Accès refusé.", "danger")
        return redirect(url_for("home"))

    product = Product.query.get_or_404(product_id)
    db.session.delete(product)
    db.session.commit()
    flash("Produit supprimé avec succès.", "success")
    return redirect(url_for("edit_products"))


@app.route("/add_category", methods=["POST"])
@login_required
def add_category():
    if current_user.role != "admin":
        flash("Accès refusé.", "danger")
        return redirect(url_for("home"))

    name = request.form["name"]
    if name:
        category = Category(name=name)
        db.session.add(category)
        db.session.commit()
        flash("Catégorie ajoutée avec succès.", "success")
    return redirect(url_for("edit_categories"))


@app.route("/delete_category/<int:category_id>", methods=["POST"])
@login_required
def delete_category(category_id):
    if current_user.role != "admin":
        flash("Accès refusé.", "danger")
        return redirect(url_for("home"))

    category = Category.query.get_or_404(category_id)
    db.session.delete(category)
    db.session.commit()
    flash("Catégorie supprimée avec succès.", "success")
    return redirect(url_for("edit_categories"))


@app.route("/edit_category/<int:category_id>", methods=["POST"])
@login_required
def edit_category(category_id):
    if current_user.role != "admin":
        flash("Accès refusé.", "danger")
        return redirect(url_for("home"))

    category = Category.query.get_or_404(category_id)
    new_name = request.form["name"]
    category.name = new_name
    db.session.commit()
    flash("Catégorie mise à jour avec succès.", "success")
    return redirect(url_for("edit_categories"))


@app.errorhandler(404)
def error_404(_):
    return render_template("404.html"), 404


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
    animals = Pet.query.filter_by(shelter_id=shelter_id).all()

    if not shelter_data:
        return render_template("404.html")

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
    shelters = Shelter.query.all()
    selected_shelter = Shelter.query.get(shelter_id) if shelter_id else None
    animals = {pet.pet_id: Animal.query.get(pet.animal_id) for pet in pets}

    return render_template(
        "adopt_animals.html",
        pets=pets,
        animals=animals,
        shelters=shelters,
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

    categories = Category.query.all()

    if category_name:
        selected_category = Category.query.filter_by(name=category_name).first()
        if selected_category:
            products_list = Product.query.filter_by(
                category_id=selected_category.category_id
            ).all()
        else:
            products_list = []
    else:
        products_list = Product.query.all()

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


@app.route("/advices")
def advices():
    return render_template("advices.html")


@app.route("/blog")
def blog():
    collection = mongo_db.miaouff_collection
    articles = collection.find()
    return render_template("blog.html", articles=articles)


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


@app.route("/cart")
def cart():
    cart = session.get("cart", [])
    return render_template("cart.html", cart=cart)


@app.route("/add_to_cart/<int:product_id>", methods=["POST"])
def add_to_cart(product_id):
    product = Product.query.get_or_404(product_id)
    data = request.get_json()
    quantity_requested = int(data.get("quantity", 1))

    cart = session.get("cart", [])

    for item in cart:
        if item["product_id"] == product_id:
            total_quantity = item["quantity"] + quantity_requested
            if total_quantity > product.stock:
                return jsonify({"success": False, "message": "Stock insuffisant"}), 400
            item["quantity"] = total_quantity
            item["total_price"] = item["quantity"] * item["price"]
            session["cart"] = cart
            return jsonify({"success": True})

    if quantity_requested > product.stock:
        return jsonify({"success": False, "message": "Stock insuffisant"}), 400

    cart.append(
        {
            "product_id": product_id,
            "name": product.name,
            "price": product.price_incl_tax,
            "quantity": quantity_requested,
            "total_price": quantity_requested * product.price_incl_tax,
            "image": product.image,
        }
    )
    session["cart"] = cart

    return jsonify({"success": True})


@app.route("/update_cart/<int:product_id>", methods=["POST"])
def update_cart(product_id):
    data = request.get_json()
    new_quantity = int(data.get("quantity", 1))

    cart = session.get("cart", [])

    for item in cart:
        if item["product_id"] == product_id:
            product = Product.query.get_or_404(product_id)
            if new_quantity > product.stock:
                return (
                    jsonify(
                        {
                            "success": False,
                            "message": "Stock insuffisant",
                            "corrected_quantity": product.stock,
                        }
                    ),
                    400,
                )
            item["quantity"] = new_quantity
            item["total_price"] = new_quantity * item["price"]
            session["cart"] = cart
            return jsonify({"success": True})

    return jsonify({"success": False, "message": "Produit non trouvé"}), 400


@app.route("/remove_from_cart/<int:product_id>", methods=["POST"])
def remove_from_cart(product_id):
    cart = session.get("cart", [])
    cart = [item for item in cart if item["product_id"] != product_id]
    session["cart"] = cart
    return redirect(url_for("cart"))


@app.route("/check_order", methods=["GET", "POST"])
@login_required
def check_order():
    user = User.query.get(current_user.user_id)
    cart = session.get("cart", [])

    if not cart:
        return redirect(url_for("cart"))

    total_excl_tax = sum(item["price"] * item["quantity"] for item in cart)
    total_incl_tax = sum(item["total_price"] for item in cart)
    shipping_fee = 5.00

    is_address_complete = all(
        [
            user.first_name,
            user.last_name,
            user.address_number,
            user.street_name,
            user.postal_code,
            user.city,
            user.country,
        ]
    )

    if is_address_complete:
        return redirect(url_for("payment"))

    return redirect(url_for("edit_address"))


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
        flash("Article créé avec succès", "success")
        return redirect(url_for("edit_articles"))

    total_articles = collection.count_documents({})
    total_pages = (total_articles + per_page - 1) // per_page
    articles = list(
        collection.find()
        .sort("created_at", -1)
        .skip((page - 1) * per_page)
        .limit(per_page)
    )
    shelters = Shelter.query.all()

    return render_template(
        "edit_articles.html",
        articles=articles,
        shelters=shelters,
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
        title = request.form["title"]
        content = request.form["content"]
        shelter_id = request.form.get("shelter_id") or None
        image = request.files.get("image")

        update_data = {
            "title": title,
            "content": content,
            "shelter_id": int(shelter_id) if shelter_id else None,
        }

        if image and image.filename != "":
            image_filename = secure_filename(image.filename)
            image.save(os.path.join(app.config["UPLOAD_FOLDER"], image_filename))
            update_data["image_url"] = f"images/{image_filename}"

        collection.update_one({"_id": ObjectId(article_id)}, {"$set": update_data})
        flash("Article mis à jour", "success")
        return redirect(url_for("edit_articles"))

    shelters = Shelter.query.all()
    return render_template("edit_article.html", article=article, shelters=shelters)


@app.route("/delete-article/<article_id>", methods=["POST"])
@login_required
def delete_article(article_id):
    if current_user.role != "admin":
        flash("Accès refusé.", "danger")
        return redirect(url_for("home"))

    collection = mongo_db.miaouff_collection
    collection.delete_one({"_id": ObjectId(article_id)})
    flash("Article supprimé", "success")
    return redirect(url_for("edit_articles"))


@app.route("/edit_categories", methods=["GET", "POST"])
@login_required
def edit_categories():
    if current_user.role != "admin":
        flash("Accès refusé.", "danger")
        return redirect(url_for("home"))

    edit_id = request.args.get("edit", type=int)
    categories = Category.query.order_by(Category.name.asc()).all()
    for cat in categories:
        cat.editing = cat.category_id == edit_id
    return render_template("edit_categories.html", categories=categories)


@app.route("/payment")
def payment():
    return render_template("payment.html")


@app.route("/edit_address")
def edit_address():
    return render_template("edit_address.html")


def get_db_connection():
    conn = psycopg2.connect(
        dbname=os.getenv("DB_NAME"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
        host=os.getenv("DB_HOST"),
        port=os.getenv("DB_PORT"),
    )
    return conn


if __name__ == "__main__":
    app.run(debug=True)
