import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from app import app


def test_homepage():
    with app.test_client() as client:
        response = client.get("/")
        assert response.status_code == 200


def test_glossary_with_filter():
    with app.test_client() as client:
        response = client.get("/glossary?species=chat")
        assert response.status_code == 200
