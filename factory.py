"""Application factory: builds, configures and wires up the Flask app.

Using a factory keeps global state out of import time, makes testing easier
and is the idiomatic way to assemble a blueprint-based Flask application.
"""

import stripe
from flask import Flask, render_template
from flask_migrate import Migrate

from blueprints.admin import admin_bp
from blueprints.auth import auth_bp
from blueprints.main import main_bp
from blueprints.shop import shop_bp
from config import Config
from extensions import init_mongo, login_manager, mail
from flask_session import Session
from models.models import db


def create_app(config_class=Config):
    """Create and configure a Flask application instance."""
    app = Flask(__name__)
    app.config.from_object(config_class)

    # Stripe secret key, set once at startup from the config/env.
    stripe.api_key = app.config["STRIPE_SECRET_KEY"]

    _init_extensions(app)
    _register_blueprints(app)
    _register_filters(app)
    _register_error_handlers(app)

    return app


def _init_extensions(app):
    db.init_app(app)
    Migrate(app, db)
    Session(app)
    mail.init_app(app)

    login_manager.init_app(app)
    login_manager.login_view = "auth.login"
    login_manager.login_message = "Veuillez vous connecter pour accéder à cette page."
    login_manager.login_message_category = "danger"

    init_mongo(app)


def _register_blueprints(app):
    app.register_blueprint(main_bp)
    app.register_blueprint(auth_bp)
    app.register_blueprint(shop_bp)
    app.register_blueprint(admin_bp)


def _register_filters(app):
    @app.template_filter("date_fr")
    def date_fr_filter(dt):
        """Format a datetime as a French date string, e.g. '16 avril 2026'."""
        if not dt:
            return ""
        months = [
            "",
            "janvier",
            "février",
            "mars",
            "avril",
            "mai",
            "juin",
            "juillet",
            "août",
            "septembre",
            "octobre",
            "novembre",
            "décembre",
        ]
        return f"{dt.day} {months[dt.month]} {dt.year}"


def _register_error_handlers(app):
    def render_error(code, title, message):
        """Render the shared error template with the right HTTP status."""
        return (
            render_template(
                "error.html",
                error_code=code,
                error_title=title,
                error_message=message,
            ),
            code,
        )

    @app.errorhandler(401)
    def error_401(_):
        return render_error(
            401,
            "Accès refusé",
            "Vous devez être connecté pour accéder à cette page. 🔐",
        )

    @app.errorhandler(403)
    def error_403(_):
        return render_error(
            403,
            "Permission refusée",
            "Vous n'avez pas les droits nécessaires pour accéder à cette ressource.",
        )

    @app.errorhandler(404)
    def error_404(_):
        return render_error(
            404,
            "Page introuvable",
            "Oups ! On a cherché partout... même sous le canapé 🐾\n"
            "Cette page n'existe pas (ou plus).",
        )

    @app.errorhandler(429)
    def error_429(_):
        return render_error(
            429,
            "Trop de requêtes",
            "Vous avez effectué trop de tentatives en peu de temps. "
            "Patientez un instant avant de réessayer.",
        )

    @app.errorhandler(500)
    def error_500(_):
        return render_error(
            500,
            "Erreur serveur",
            "Une erreur inattendue s'est produite de notre côté. "
            "Notre équipe a été notifiée. 🛠️",
        )

    @app.errorhandler(503)
    def error_503(_):
        return render_error(
            503,
            "Service indisponible",
            "Le site est temporairement indisponible pour maintenance. "
            "Revenez dans quelques minutes.",
        )
