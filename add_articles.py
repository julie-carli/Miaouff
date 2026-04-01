from pymongo import MongoClient
from datetime import datetime
import os
from dotenv import load_dotenv


load_dotenv()
mongo_uri = os.getenv("MONGODB_URI")
client = MongoClient(mongo_uri)
db = client["miaouff_database"]
articles_collection = db["miaouff_collection"]

articles = [
    {
        "title": "Adoption de Mia au Havre des Ronronnements",
        "content": (
            "Nous avons une merveilleuse nouvelle à partager ! Mia, une petite chatte abandonnée dans la rue, a été adoptée par une famille aimante. "
            "Après avoir été recueillie, soignée et choyée par notre équipe, Mia a retrouvé toute sa joie de vivre. Aujourd'hui, elle coule des jours heureux "
            "dans son nouveau foyer, entourée de beaucoup d'amour. Cela prouve que chaque animal mérite une chance de connaître le bonheur. "
            "Venez rencontrer nos autres petits pensionnaires au Havre des Ronronnements, peut-être que l'un d'entre eux sera votre futur compagnon !"
        ),
        "image_url": "images/mia.png",
        "shelter_id": 1,
        "created_at": datetime.now(),
    },
    {
        "title": "Adoption de Rex au Refuge des Câlins Canins",
        "content": (
            "Rex, un chien sauvé de l'euthanasie, a trouvé une nouvelle vie grâce à l'amour et à la détermination de ses nouveaux propriétaires. "
            "Il a été adopté et vit désormais dans une maison pleine de câlins et de jeux. Nous sommes ravis de voir Rex heureux et en pleine forme. "
            "Son histoire démontre qu'il n'est jamais trop tard pour offrir une nouvelle chance à un animal. "
            "Venez découvrir les autres chiens qui attendent avec impatience leur famille au Refuge des Câlins Canins."
        ),
        "image_url": "images/rex.png",
        "shelter_id": 2,
        "created_at": datetime.now(),
    },
    {
        "title": "Rénovation des refuges : Venez découvrir nos petits pensionnaires",
        "content": (
            "Nous sommes heureux d'annoncer que les deux refuges Le Havre des Ronronnements et Le Refuge des Câlins Canins ont récemment subi des rénovations majeures. "
            "Ces travaux ont permis d'améliorer les conditions de vie de nos animaux et d'offrir des espaces plus adaptés à leurs besoins. "
            "Nous invitons tous les amoureux des animaux à venir découvrir nos refuges rénovés et rencontrer nos petits pensionnaires qui attendent une nouvelle famille. "
            "Grâce à votre soutien, nous continuons d'offrir une vie meilleure à nos animaux."
        ),
        "image_url": "images/renovation-refuge.png",
        "shelter_id": None,
        "created_at": datetime.now(),
    },
]

articles_collection.insert_many(articles)

print("Les articles ont été ajoutés avec succès !")
