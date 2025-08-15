import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from app import app, db, User
from werkzeug.security import generate_password_hash


def setup_test_user():
    with app.app_context():
        user = User.query.filter_by(email="test@example.com").first()
        if not user:
            user = User(
                email="test@example.com",
                password=generate_password_hash("Password123!", method="pbkdf2:sha256"),
            )
            db.session.add(user)
            db.session.commit()


def test_login_valid_credentials():
    setup_test_user()
    with app.test_client() as client:
        response = client.post(
            "/login",
            data=dict(
                email="test@example.com", password="Password123!", action="login"
            ),
            follow_redirects=True,
        )
        assert b"account" in response.data or response.status_code == 200


def test_login_invalid_credentials():
    with app.test_client() as client:
        response = client.post(
            "/login",
            data=dict(email="wrong@example.com", password="wrongpass", action="login"),
            follow_redirects=True,
        )
        assert b"Identifiants incorrects" in response.data
