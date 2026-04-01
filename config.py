import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()


class Config:
    # ============================
    # Security
    # ============================
    SECRET_KEY = os.getenv("SECRET_KEY")

    # ============================
    # PostgreSQL / SQLAlchemy
    # ============================
    SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URL")
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # ============================
    # Session
    # ============================
    SESSION_TYPE = "filesystem"

    # ============================
    # File uploads
    # ============================
    BASE_DIR = os.path.abspath(os.path.dirname(__file__))
    UPLOAD_FOLDER = os.path.join(BASE_DIR, "static", "images")
    ALLOWED_EXTENSIONS = {"png", "jpg", "jpeg", "gif"}

    # ============================
    # Email (Flask-Mail)
    # ============================
    MAIL_SERVER = os.getenv("MAIL_SERVER")
    MAIL_PORT = int(os.getenv("MAIL_PORT", 587))
    MAIL_USE_TLS = os.getenv("MAIL_USE_TLS", "True") == "True"
    MAIL_USERNAME = os.getenv("MAIL_USERNAME")
    MAIL_PASSWORD = os.getenv("MAIL_PASSWORD")
    MAIL_DEFAULT_SENDER = os.getenv("MAIL_DEFAULT_SENDER")

    # ============================
    # MongoDB
    # ============================
    MONGODB_URI = os.getenv("MONGODB_URI")