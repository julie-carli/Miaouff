import os

from dotenv import load_dotenv
from flask import Flask

from setup_db import db

app = Flask(__name__)

load_dotenv()


app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("DATABASE_URL")
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False


db.init_app(app)


with app.app_context():
    db.drop_all()
    print("Toutes les tables ont été supprimées.")
