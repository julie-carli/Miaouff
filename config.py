import os
from datetime import timedelta

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
    # Session & cookie security
    # ============================
    SESSION_TYPE = "filesystem"
    # Cookies are never exposed to JavaScript and are scoped to same-site
    # navigation, which mitigates XSS cookie theft and CSRF.
    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SAMESITE = "Lax"
    # Secure flag (HTTPS only) is on by default; disabled in local/CI HTTP via
    # SESSION_COOKIE_SECURE=False.
    SESSION_COOKIE_SECURE = os.getenv("SESSION_COOKIE_SECURE", "True") == "True"
    PERMANENT_SESSION_LIFETIME = timedelta(days=7)
    # Reject request bodies larger than 5 MB (also caps file uploads).
    MAX_CONTENT_LENGTH = 5 * 1024 * 1024

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

    # ============================
    # Stripe
    # ============================
    STRIPE_PUBLIC_KEY = os.getenv("STRIPE_PUBLIC_KEY")
    STRIPE_SECRET_KEY = os.getenv("STRIPE_SECRET_KEY")

    # ============================
    # Analytics (Google Analytics 4)
    # ============================
    # Measurement id (e.g. "G-XXXXXXXXXX"). Empty by default, so no analytics
    # script is loaded until both an id is set and the user gives consent.
    GA_MEASUREMENT_ID = os.getenv("GA_MEASUREMENT_ID", "")
