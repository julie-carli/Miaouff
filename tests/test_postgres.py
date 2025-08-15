import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from setup_db import Category
from app import app


def test_postgres_connection():
    with app.app_context():
        categories = Category.query.all()
        assert isinstance(categories, list)
