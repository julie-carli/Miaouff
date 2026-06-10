"""Public-facing pages: home, catalogue, adoption, blog, glossary, games."""

from bson import ObjectId
from flask import (
    Blueprint,
    Response,
    jsonify,
    render_template,
    request,
    session,
    url_for,
)

from extensions import articles_collection
from models.models import Animal, Pet, Product, Shelter
from services.chat_service import send_message_to_make
from services.product_service import get_products_by_category

main_bp = Blueprint("main", __name__)


@main_bp.route("/")
def home():
    return render_template("home.html")


@main_bp.route("/chat", methods=["POST"])
def chat():
    data = request.get_json()
    user_message = data.get("message", "").strip()
    history = data.get("history", [])

    if not user_message:
        return jsonify({"success": False, "response": "Message vide."}), 400

    bot_response = send_message_to_make(user_message, history)
    return jsonify({"success": True, "response": bot_response})


@main_bp.route("/glossary")
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


@main_bp.route("/glossary/<int:animal_id>")
def glossary_animal(animal_id):
    animal = Animal.query.get_or_404(animal_id)
    return render_template("glossary_animal.html", animal=animal)


@main_bp.route("/shelters")
def shelters():
    shelters_data = Shelter.query.all()
    return render_template("shelters.html", shelters=shelters_data)


@main_bp.route("/shelter/<int:shelter_id>")
def shelter(shelter_id):
    shelter_data = Shelter.query.get(shelter_id)
    if not shelter_data:
        return render_template("404.html")
    animals = Pet.query.filter_by(shelter_id=shelter_id).all()
    return render_template("shelter.html", shelter=shelter_data, animals=animals)


@main_bp.route("/adopt-animals")
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


@main_bp.route("/adopt-animal/<int:pet_id>")
def adopt_animal(pet_id):
    pet = Pet.query.get_or_404(pet_id)
    animal = Animal.query.get(pet.animal_id)
    return render_template("adopt_animal.html", pet=pet, animal=animal)


@main_bp.route("/animals")
def animals():
    return render_template("animals.html")


@main_bp.route("/products")
def products():
    category_name = request.args.get("category")
    products_list, categories = get_products_by_category(category_name)
    return render_template(
        "products.html",
        products=products_list,
        categories=categories,
        selected_category=category_name,
    )


@main_bp.route("/product/<int:product_id>")
def product(product_id):
    product_item = Product.query.get_or_404(product_id)
    return render_template("product.html", product=product_item)


@main_bp.route("/blog")
def blog():
    collection = articles_collection()
    page = request.args.get("page", 1, type=int)
    per_page = 9

    total_articles = collection.count_documents({})
    total_pages = (total_articles + per_page - 1) // per_page

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


@main_bp.route("/blog/<article_id>")
def blog_article(article_id):
    collection = articles_collection()
    article = collection.find_one({"_id": ObjectId(article_id)})

    if not article:
        return (
            render_template(
                "error.html",
                error_code=404,
                error_title="Article introuvable",
                error_message="Cet article n'existe pas ou a été supprimé.",
            ),
            404,
        )

    return render_template("blog_article.html", article=article)


@main_bp.route("/contact")
def contact():
    return render_template("contact.html")


@main_bp.route("/faq")
def faq():
    return render_template("faq.html")


@main_bp.route("/privacy_policy")
def privacy_policy():
    return render_template("privacy_policy.html")


@main_bp.route("/cookie_policy")
def cookie_policy():
    return render_template("cookie_policy.html")


@main_bp.route("/legal_notices")
def legal_notices():
    return render_template("legal_notices.html")


@main_bp.route("/terms_conditions")
def terms_conditions():
    return render_template("terms_conditions.html")


@main_bp.route("/games")
def games():
    return render_template("games.html")


@main_bp.route("/quiz")
def quiz():
    return render_template("quiz.html")


@main_bp.route("/match")
def match():
    return render_template("match.html")


@main_bp.route("/memory")
def memory():
    return render_template("memory.html")


@main_bp.route("/wordsearch")
def wordsearch():
    return render_template("wordsearch.html")


@main_bp.route("/hangman")
def hangman():
    return render_template("hangman.html")


@main_bp.route("/rapido")
def rapido():
    return render_template("rapido.html")


@main_bp.route("/robots.txt")
def robots():
    """Serve robots.txt: allow public pages, keep admin/account out of indexes."""
    lines = [
        "User-agent: *",
        "Disallow: /edit-",
        "Disallow: /edit_",
        "Disallow: /delete",
        "Disallow: /account",
        f"Sitemap: {request.url_root}sitemap.xml",
        "",
    ]
    return Response("\n".join(lines), mimetype="text/plain")


@main_bp.route("/sitemap.xml")
def sitemap():
    """Serve a sitemap listing the public, indexable pages."""
    endpoints = [
        "main.home",
        "main.shelters",
        "main.animals",
        "main.adopt_animals",
        "main.products",
        "main.blog",
        "main.glossary",
        "main.games",
        "main.contact",
        "main.faq",
        "main.privacy_policy",
        "main.legal_notices",
        "main.terms_conditions",
        "main.cookie_policy",
    ]
    xml = [
        '<?xml version="1.0" encoding="UTF-8"?>',
        '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">',
    ]
    for endpoint in endpoints:
        xml.append(f"  <url><loc>{url_for(endpoint, _external=True)}</loc></url>")
    xml.append("</urlset>")
    return Response("\n".join(xml), mimetype="application/xml")


@main_bp.app_context_processor
def cart_count():
    """Expose the cart item count to every template."""
    cart = session.get("cart", [])
    count = sum(item.get("quantity", 0) for item in cart)
    return {"cart_count": count}
