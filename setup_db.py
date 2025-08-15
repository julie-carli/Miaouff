from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin
from dotenv import load_dotenv
import os
from sqlalchemy import (
    create_engine,
    Column,
    Integer,
    String,
    Text,
    Date,
    ForeignKey,
    TIMESTAMP,
    Float,
)
from sqlalchemy.dialects.postgresql import NUMERIC
from sqlalchemy.orm import relationship, sessionmaker
from werkzeug.security import generate_password_hash, check_password_hash

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")

app = Flask(__name__)
app.secret_key = os.getenv("SECRET_KEY")
app.config["SQLALCHEMY_DATABASE_URI"] = DATABASE_URL
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)
login_manager = LoginManager(app)
login_manager.login_view = "login"


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class Shelter(db.Model):
    __tablename__ = "shelters"
    shelter_id = Column(Integer, primary_key=True)
    name = Column(String(255), nullable=False)
    address = Column(Text, nullable=False)
    phone = Column(String(20), nullable=False)
    email = Column(String(255), nullable=False)
    description = Column(Text)
    image = Column(String(200))
    pets = relationship("Pet", back_populates="shelter")


class Animal(db.Model):
    __tablename__ = "animals"
    animal_id = Column(Integer, primary_key=True)
    species = Column(String(100), nullable=False)
    breed = Column(String(100), nullable=False)
    lifespan = Column(String(50))
    diet = Column(Text)
    specifics = Column(Text)
    image = Column(String(200))
    pets = relationship("Pet", back_populates="animal")


class Pet(db.Model):
    __tablename__ = "pets"
    pet_id = Column(Integer, primary_key=True)
    name = Column(String(255), nullable=False)
    age = Column(Integer, nullable=False)
    gender = Column(String(10), nullable=False)
    description = Column(Text)
    adoption_date = Column(Date, nullable=True)
    image = Column(String(200))
    shelter_id = Column(Integer, ForeignKey("shelters.shelter_id"))
    animal_id = Column(Integer, ForeignKey("animals.animal_id"))
    shelter = relationship("Shelter", back_populates="pets")
    animal = relationship("Animal", back_populates="pets")


class Category(db.Model):
    __tablename__ = "categories"
    category_id = Column(Integer, primary_key=True)
    name = Column(String(255), nullable=False)
    products = relationship("Product", back_populates="category")


class Product(db.Model):
    __tablename__ = "products"
    product_id = Column(Integer, primary_key=True)
    name = Column(String(255), nullable=False)
    description = Column(Text)
    price_excl_tax = Column(NUMERIC(10, 2), nullable=False)
    price_incl_tax = Column(NUMERIC(10, 2), nullable=False)
    stock = Column(Integer, nullable=False)
    weight = Column(NUMERIC(10, 2), nullable=False)
    image = Column(String(200))
    category_id = Column(Integer, ForeignKey("categories.category_id"))
    category = relationship("Category", back_populates="products")
    order_products = relationship("OrderProduct", back_populates="product")


class User(db.Model, UserMixin):
    """
    User model representing an application user.

    Attributes:
        user_id (int): Primary key, unique identifier for the user.
        first_name (str): User's first name.
        last_name (str): User's last name.
        email (str): User's email address, unique and required.
        password (str): Hashed password of the user, stored securely.
        address_number (str): User's street number.
        street_name (str): Name of the street for user's address.
        address_complement (str): Additional address information.
        postal_code (str): Postal code of the user's address.
        city (str): City of the user's address.
        country (str): Country of the user's address.
        phone (str): User's phone number.
        role (str): Role of the user in the system, defaults to "user".
        birth_date (date): User's date of birth.
        orders (relationship): Relationship to Order objects linked to the user.
    """

    __tablename__ = "users"
    user_id = Column(Integer, primary_key=True)
    first_name = Column(String(255))
    last_name = Column(String(255))
    email = Column(String(255), unique=True, nullable=False)
    password = Column(Text, nullable=False)  # Stored as a hashed password
    address_number = Column(String(10))
    street_name = Column(String(255))
    address_complement = Column(String(255))
    postal_code = Column(String(10))
    city = Column(String(100))
    country = Column(String(100))
    phone = Column(String(20))
    role = Column(
        String(50), nullable=False, default="user"
    )  # User role: 'user' or 'admin'
    birth_date = Column(Date)
    orders = relationship(
        "Order", back_populates="user"
    )  # One-to-many relationship with orders

    def get_id(self):
        """
        Return the unique identifier of the user as a string.

        Returns:
            str: The user_id converted to string.
        """
        return str(self.user_id)


class Order(db.Model):
    __tablename__ = "orders"
    order_id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.user_id"))
    order_date = Column(TIMESTAMP, nullable=False)
    status = Column(String(50), nullable=False)
    total_price_excl_tax = Column(NUMERIC(10, 2), nullable=False)
    total_price_incl_tax = Column(NUMERIC(10, 2), nullable=False)
    shipping_fee = Column(NUMERIC(10, 2), nullable=False)
    order_products = relationship("OrderProduct", back_populates="order")
    user = relationship("User", back_populates="orders")
    payments = db.relationship("Payment", back_populates="order")


class OrderProduct(db.Model):
    __tablename__ = "order_products"
    order_id = Column(Integer, ForeignKey("orders.order_id"), primary_key=True)
    product_id = Column(Integer, ForeignKey("products.product_id"), primary_key=True)
    quantity = Column(Integer, nullable=False)
    unit_price_excl_tax = Column(NUMERIC(10, 2), nullable=False)
    unit_price_incl_tax = Column(NUMERIC(10, 2), nullable=False)
    order = relationship("Order", back_populates="order_products")
    product = relationship("Product", back_populates="order_products")


class Payment(db.Model):
    __tablename__ = "payments"
    payment_id = Column(Integer, primary_key=True)
    payment_method = Column(String(50))
    payment_status = Column(String(50))
    payment_date = Column(TIMESTAMP, nullable=False)
    payment_total = Column(Float, nullable=False)
    order_id = Column(Integer, ForeignKey("orders.order_id"))
    order = relationship("Order", back_populates="payments")


def create_tables():
    with app.app_context():
        db.create_all()
    print("Tables created in db.")


if __name__ == "__main__":
    create_tables()
    print("DB and tables ready!")


shelters = [
    {
        "name": "Le Havre des Ronronnements",
        "address": "12 Rue des Chats Heureux, 28000 Chartres, France",
        "phone": "+33 2 37 00 00 00",
        "email": "havre-ronronnements@miaouff.fr",
        "description": "Un refuge chaleureux dédié aux chats en attente d'une famille aimante.",
        "image": "the_haven_of_purrs.png",
    },
    {
        "name": "Le Refuge des Câlins Canins",
        "address": "25 Avenue des Amis Fidèles, 28100 Dreux, France",
        "phone": "+33 2 37 11 11 11",
        "email": "refuge-calins-canins@miaouff.fr",
        "description": "Un havre de paix pour chiens abandonnés, en quête d'un nouveau foyer.",
        "image": "the_canine_cuddle_shelter.png",
    },
]

categories = [
    {"category_name": "Alimentation"},
    {"category_name": "Jouets"},
    {"category_name": "Hygiène"},
    {"category_name": "Autres"},
]

products = [
    {
        "product_name": "Croquettes Énergie+",
        "product_type": "Croquettes pour chien",
        "product_description": "Des croquettes riches en nutriments pour une vitalité optimale.",
        "price_excl_tax": round(29.99 / 1.2, 2),
        "price_incl_tax": 29.99,
        "stock": 100,
        "weight": 5.0,
        "image": "images/croquettes.png",
        "category_name": "Alimentation",
    },
    {
        "product_name": "Délice Gourmet Félin",
        "product_type": "Pâtée pour chat",
        "product_description": "Une pâtée savoureuse et équilibrée pour chats exigeants.",
        "price_excl_tax": round(2.99 / 1.2, 2),
        "price_incl_tax": 2.99,
        "stock": 200,
        "weight": 0.3,
        "image": "images/patee.png",
        "category_name": "Alimentation",
    },
    {
        "product_name": "Os à Ronger Saveur Bœuf",
        "product_type": "Os à ronger pour chien",
        "product_description": "Un os savoureux qui aide à l’hygiène dentaire de votre chien.",
        "price_excl_tax": round(5.49 / 1.2, 2),
        "price_incl_tax": 5.49,
        "stock": 80,
        "weight": 0.6,
        "image": "images/os.png",
        "category_name": "Alimentation",
    },
    {
        "product_name": "Savon Douceur Animale",
        "product_type": "Savon",
        "product_description": "Un savon doux pour nettoyer et hydrater la peau de votre compagnon.",
        "price_excl_tax": round(7.99 / 1.2, 2),
        "price_incl_tax": 7.99,
        "stock": 50,
        "weight": 0.2,
        "image": "images/savon.png",
        "category_name": "Hygiène",
    },
    {
        "product_name": "Gant Attrape-Poils",
        "product_type": "Gant de toilettage",
        "product_description": "Un gant pratique pour enlever les poils morts de votre animal.",
        "price_excl_tax": round(12.99 / 1.2, 2),
        "price_incl_tax": 12.99,
        "stock": 120,
        "weight": 0.3,
        "image": "images/gant.png",
        "category_name": "Hygiène",
    },
    {
        "product_name": "Litière Confort+",
        "product_type": "Litière",
        "product_description": "Litière absorbante et anti-odeurs pour le bien-être de votre chat.",
        "price_excl_tax": round(15.99 / 1.2, 2),
        "price_incl_tax": 15.99,
        "stock": 60,
        "weight": 10.0,
        "image": "images/litiere.png",
        "category_name": "Hygiène",
    },
    {
        "product_name": "Haltère Bleu Musclé",
        "product_type": "Jouet pour chien",
        "product_description": "Un haltère en caoutchouc robuste pour muscler et divertir votre chien.",
        "price_excl_tax": round(8.99 / 1.2, 2),
        "price_incl_tax": 8.99,
        "stock": 90,
        "weight": 0.7,
        "image": "images/haltere.png",
        "category_name": "Jouets",
    },
    {
        "product_name": "Poisson Sautillant",
        "product_type": "Jouet pour chat",
        "product_description": "Un jouet en forme de poisson qui bouge pour stimuler votre chat.",
        "price_excl_tax": round(6.99 / 1.2, 2),
        "price_incl_tax": 6.99,
        "stock": 100,
        "weight": 0.2,
        "image": "images/poisson-jouet.png",
        "category_name": "Jouets",
    },
    {
        "product_name": "Tour de Jeu Féli'Fun",
        "product_type": "Jouet interactif pour chat",
        "product_description": "Un jouet avec trois étages et une balle par niveau pour divertir votre chat.",
        "price_excl_tax": round(14.99 / 1.2, 2),
        "price_incl_tax": 14.99,
        "stock": 75,
        "weight": 0.9,
        "image": "images/roulette.png",
        "category_name": "Jouets",
    },
    {
        "product_name": "Don pour le Refuge",
        "product_type": "Don",
        "product_description": "Faites un don pour soutenir les animaux en refuge.",
        "price_excl_tax": 5.00,
        "price_incl_tax": 5.00,
        "stock": 9999,
        "weight": 0.0,
        "image": "images/don.png",
        "category_name": "Autres",
    },
]

pets = [
    {
        "pet_name": "Mew",
        "pet_age": 2,
        "pet_gender": "Mâle",
        "pet_description": "Un adorable chat joueur et curieux qui adore les câlins.",
        "pet_adoption_date": None,
        "pet_image": "images/mew.png",
        "animal_breed": "Chat européen",
        "shelter_name": "Le Havre des Ronronnements",
    },
    {
        "pet_name": "Minou",
        "pet_age": 4,
        "pet_gender": "Mâle",
        "pet_description": "Un chat doux et calme qui aime se prélasser au soleil.",
        "pet_adoption_date": None,
        "pet_image": "images/minou.png",
        "animal_breed": "Chat européen",
        "shelter_name": "Le Havre des Ronronnements",
    },
    {
        "pet_name": "Chippie",
        "pet_age": 1,
        "pet_gender": "Femelle",
        "pet_description": "Petite boule d'énergie, Chippie adore jouer et grimper partout.",
        "pet_adoption_date": None,
        "pet_image": "images/chippie.png",
        "animal_breed": "Chat européen",
        "shelter_name": "Le Havre des Ronronnements",
    },
    {
        "pet_name": "Max",
        "pet_age": 3,
        "pet_gender": "Mâle",
        "pet_description": "Max est un chien affectueux et protecteur, idéal pour une famille.",
        "pet_adoption_date": None,
        "pet_image": "images/max.png",
        "animal_breed": "Labrador",
        "shelter_name": "Le Refuge des Câlins Canins",
    },
    {
        "pet_name": "Tonnerre",
        "pet_age": 5,
        "pet_gender": "Mâle",
        "pet_description": "Un chien énergique et joueur qui adore courir et se dépenser.",
        "pet_adoption_date": None,
        "pet_image": "images/tonnerre.png",
        "animal_breed": "Husky",
        "shelter_name": "Le Refuge des Câlins Canins",
    },
    {
        "pet_name": "Daisy",
        "pet_age": 2,
        "pet_gender": "Femelle",
        "pet_description": "Daisy est une chienne douce et sociable qui adore les enfants.",
        "pet_adoption_date": None,
        "pet_image": "images/daisy.png",
        "animal_breed": "Chihuahua",
        "shelter_name": "Le Refuge des Câlins Canins",
    },
]

animals = [
    {
        "animal_species": "Chien",
        "animal_breed": "Labrador",
        "animal_lifespan": "10-14 ans",
        "animal_diet": "Croquettes, pâtée, alimentation équilibrée.",
        "animal_specifics": "Chien intelligent, affectueux et joueur, idéal pour les familles.",
        "animal_image": "images/labrador.png",
    },
    {
        "animal_species": "Chien",
        "animal_breed": "Chihuahua",
        "animal_lifespan": "12-20 ans",
        "animal_diet": "Croquettes adaptées aux petites races, parfois complémentée de nourriture humide.",
        "animal_specifics": "Petit chien vif et attachant, très fidèle à son maître.",
        "animal_image": "images/chihuahua.png",
    },
    {
        "animal_species": "Chien",
        "animal_breed": "Husky",
        "animal_lifespan": "12-15 ans",
        "animal_diet": "Alimentation riche en protéines, adaptée aux chiens très actifs.",
        "animal_specifics": "Chien énergique, intelligent et sociable, nécessite beaucoup d'exercice.",
        "animal_image": "images/husky.png",
    },
    {
        "animal_species": "Chat",
        "animal_breed": "Maine Coon",
        "animal_lifespan": "12-15 ans",
        "animal_diet": "Croquettes premium, viande et poisson occasionnellement.",
        "animal_specifics": "Grand chat affectueux, joueur et très sociable, aime l'eau.",
        "animal_image": "images/maine_coon.png",
    },
    {
        "animal_species": "Chat",
        "animal_breed": "Chat Européen",
        "animal_lifespan": "12-18 ans",
        "animal_diet": "Croquettes équilibrées, alimentation variée.",
        "animal_specifics": "Chat robuste et adaptable, sociable et indépendant.",
        "animal_image": "images/chat_europeen.png",
    },
    {
        "animal_species": "Chat",
        "animal_breed": "Angora",
        "animal_lifespan": "12-16 ans",
        "animal_diet": "Alimentation équilibrée avec des compléments pour le pelage.",
        "animal_specifics": "Chat élégant, joueur et très attaché à son humain.",
        "animal_image": "images/angora.png",
    },
]

with app.app_context():
    category_mapping = {}
    shelter_mapping = {}
    pet_mapping = {}

    for category_data in categories:
        category_name = category_data.pop("category_name", None)
        if not category_name:
            print(f"⚠️ Erreur : Key 'category_name' missing in {category_data}.")
            continue

        existing_category = Category.query.filter_by(name=category_name).first()

        if not existing_category:
            category = Category(name=category_name, **category_data)
            db.session.add(category)
            category_mapping[category_name] = category
        else:
            category_mapping[category_name] = existing_category

    db.session.commit()

    for shelter_data in shelters:
        shelter_name = shelter_data.pop("name", None)
        if not shelter_name:
            print(f"⚠️ Error : Key 'name' missing in {shelter_data}.")
            continue

        existing_shelter = Shelter.query.filter_by(name=shelter_name).first()

        if not existing_shelter:
            shelter = Shelter(name=shelter_name, **shelter_data)
            db.session.add(shelter)
            shelter_mapping[shelter_name] = shelter
        else:
            shelter_mapping[shelter_name] = existing_shelter

    db.session.commit()

    for product in products:
        existing_product = Product.query.filter_by(
            name=product.get("product_name")
        ).first()

        if not existing_product:
            category_name = product.pop("category_name", None)
            if not category_name or category_name not in category_mapping:
                print(
                    f"⚠️ Erreur : Category '{category_name}' not found for the product {product}."
                )
                continue

            category = category_mapping[category_name]
            product["category_id"] = category.category_id
            product["name"] = product.pop("product_name", None)
            product["description"] = product.pop("product_description", None)

            unwanted_keys = ["product_type"]
            for key in unwanted_keys:
                product.pop(key, None)

            new_product = Product(**product)
            db.session.add(new_product)

    db.session.commit()

    for animal_data in animals:
        existing_animal = Animal.query.filter(
            Animal.breed.ilike(animal_data["animal_breed"])
        ).first()

        if not existing_animal:
            new_animal = Animal(
                species=animal_data["animal_species"],
                breed=animal_data["animal_breed"],
                lifespan=animal_data.get("animal_lifespan"),
                diet=animal_data.get("animal_diet"),
                specifics=animal_data.get("animal_specifics"),
                image=animal_data.get("animal_image"),
            )
            db.session.add(new_animal)

    db.session.commit()

    for pet_data in pets:
        pet_name = pet_data.pop("pet_name", None)
        if not pet_name:
            print(f"⚠️ Error : Key 'pet_name' missing in {pet_data}.")
            continue

        pet_data["age"] = pet_data.pop("pet_age", None)
        pet_data["gender"] = pet_data.pop("pet_gender", None)
        pet_data["description"] = pet_data.pop("pet_description", None)
        pet_data["adoption_date"] = pet_data.pop("pet_adoption_date", None)
        pet_data["image"] = pet_data.pop("pet_image", None)

        shelter_name = pet_data.pop("shelter_name", None)
        shelter = (
            Shelter.query.filter_by(name=shelter_name).first() if shelter_name else None
        )
        if not shelter:
            print(f"⚠️ Error : No shelter found for '{shelter_name}'.")
            continue
        pet_data["shelter"] = shelter

        animal_breed = pet_data.pop("animal_breed", None)
        if not animal_breed:
            print(f"⚠️ Error : 'animal_breed' missing for {pet_name}.")
            continue

        animal = Animal.query.filter(Animal.breed.ilike(animal_breed)).first()

        if not animal:
            print(f"⚠️ Error : No animal for breed '{animal_breed}'.")
            continue
        pet_data["animal_id"] = animal.animal_id

        print(f"✅ Animal found : '{animal_breed}' → ID {animal.animal_id}")

        existing_pet = Pet.query.filter_by(name=pet_name).first()

        if not existing_pet:
            pet = Pet(name=pet_name, **pet_data)
            db.session.add(pet)
            pet_mapping[pet_name] = pet
            print(f"✅ Pet added : {pet_name}")
        else:
            pet_mapping[pet_name] = existing_pet
            print(f"ℹ️ Pet already existing : {pet_name}")

    db.session.commit()

    admin_email = os.getenv("ADMIN_EMAIL")
    admin_password = os.getenv("ADMIN_PASSWORD")

    if not admin_email or not admin_password:
        raise ValueError("ADMIN_EMAIL and ADMIN_PASSWORD should be defined in .env")

    existing_admin = User.query.filter_by(email=admin_email).first()

    if not existing_admin:
        admin = User(
            email=admin_email,
            password=generate_password_hash(admin_password, method="pbkdf2:sha256"),
            role="admin",
        )
        db.session.add(admin)
        db.session.commit()
        print("Admin created.")
    else:
        print("Admin already existing.")
    db.session.commit()

if __name__ == "__main__":
    print("✅ Add to db!")
