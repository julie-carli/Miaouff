from setup_db import db
from flask import Flask
import os
from dotenv import load_dotenv


app = Flask(__name__)

load_dotenv()


app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("DATABASE_URL")
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False


db.init_app(app)


with app.app_context():
    db.drop_all()
    print("Toutes les tables ont été supprimées.")
