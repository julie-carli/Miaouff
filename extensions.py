"""Flask extensions instantiated once and wired up by the application factory.

Keeping the extension objects here (rather than in the app module) avoids
circular imports between the factory, the blueprints and the models.
"""

from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from flask_login import LoginManager
from flask_mail import Mail
from flask_wtf import CSRFProtect
from pymongo import MongoClient

# Models can be imported without an app context; User is needed by load_user.
from models.models import User

login_manager = LoginManager()
mail = Mail()
csrf = CSRFProtect()

# Rate limiter, keyed by client IP. In-memory storage is enough for this
# project; a shared store (e.g. Redis) would be used for a multi-instance prod.
limiter = Limiter(
    key_func=get_remote_address,
    storage_uri="memory://",
)

# MongoDB handles, populated by init_mongo() during application creation.
mongo_client = None
mongo_db = None


def init_mongo(app):
    """Open the MongoDB connection and expose the database handle."""
    global mongo_client, mongo_db
    mongo_client = MongoClient(app.config["MONGODB_URI"])
    mongo_db = mongo_client.get_database()


def articles_collection():
    """Return the MongoDB collection storing blog articles."""
    return mongo_db.miaouff_collection


@login_manager.user_loader
def load_user(user_id):
    """Load a user from the database by id for session management."""
    return User.query.get(int(user_id))
