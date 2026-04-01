from flask import Flask
from dotenv import load_dotenv
from werkzeug.security import generate_password_hash
import os

from models.models import db, User, Shelter, Animal, Pet, Category, Product

# Load environment variables before anything else
load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = DATABASE_URL
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.secret_key = os.getenv("SECRET_KEY")

db.init_app(app)


def create_tables():
    """Create all database tables if they don't exist yet."""
    with app.app_context():
        db.create_all()
    print("Tables created successfully.")


# ============================
# Seed data
# ============================
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
        "product_description": "Un os savoureux qui aide à l'hygiène dentaire de votre chien.",
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


def seed_data():
    """Populate the database with initial data, skipping existing records."""
    with app.app_context():
        category_mapping = {}
        shelter_mapping = {}

        # Seed categories
        for category_data in categories:
            category_name = category_data["category_name"]
            existing = Category.query.filter_by(name=category_name).first()
            if not existing:
                category = Category(name=category_name)
                db.session.add(category)
                category_mapping[category_name] = category
            else:
                category_mapping[category_name] = existing
        db.session.commit()

        # Seed shelters
        for shelter_data in shelters:
            shelter_name = shelter_data["name"]
            existing = Shelter.query.filter_by(name=shelter_name).first()
            if not existing:
                shelter = Shelter(**{k: v for k, v in shelter_data.items()})
                db.session.add(shelter)
                shelter_mapping[shelter_name] = shelter
            else:
                shelter_mapping[shelter_name] = existing
        db.session.commit()

        # Seed products
        for product_data in products:
            product_name = product_data.get("product_name")
            if not Product.query.filter_by(name=product_name).first():
                category_name = product_data.get("category_name")
                category = category_mapping.get(category_name)
                if not category:
                    print(f"Category not found for product: {product_name}")
                    continue

                new_product = Product(
                    name=product_name,
                    description=product_data.get("product_description"),
                    price_excl_tax=product_data["price_excl_tax"],
                    price_incl_tax=product_data["price_incl_tax"],
                    stock=product_data["stock"],
                    weight=product_data["weight"],
                    image=product_data.get("image"),
                    category_id=category.category_id,
                )
                db.session.add(new_product)
        db.session.commit()

        # Seed animals
        for animal_data in animals:
            existing = Animal.query.filter(
                Animal.breed.ilike(animal_data["animal_breed"])
            ).first()
            if not existing:
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

        # Seed pets
        for pet_data in pets:
            pet_name = pet_data["pet_name"]
            if Pet.query.filter_by(name=pet_name).first():
                continue

            shelter = Shelter.query.filter_by(name=pet_data["shelter_name"]).first()
            animal = Animal.query.filter(
                Animal.breed.ilike(pet_data["animal_breed"])
            ).first()

            if not shelter or not animal:
                print(f"Shelter or animal not found for pet: {pet_name}")
                continue

            new_pet = Pet(
                name=pet_name,
                age=pet_data["pet_age"],
                gender=pet_data["pet_gender"],
                description=pet_data.get("pet_description"),
                adoption_date=pet_data.get("pet_adoption_date"),
                image=pet_data.get("pet_image"),
                shelter_id=shelter.shelter_id,
                animal_id=animal.animal_id,
            )
            db.session.add(new_pet)
        db.session.commit()

        # Seed admin user from environment variables
        admin_email = os.getenv("ADMIN_EMAIL")
        admin_password = os.getenv("ADMIN_PASSWORD")

        if not admin_email or not admin_password:
            raise ValueError(
                "ADMIN_EMAIL and ADMIN_PASSWORD must be set in the .env file."
            )

        if not User.query.filter_by(email=admin_email).first():
            admin = User(
                email=admin_email,
                password=generate_password_hash(admin_password, method="pbkdf2:sha256"),
                role="admin",
            )
            db.session.add(admin)
            db.session.commit()
            print("Admin user created successfully.")
        else:
            print("Admin user already exists.")


if __name__ == "__main__":
    create_tables()
    seed_data()
    print("Database ready.")