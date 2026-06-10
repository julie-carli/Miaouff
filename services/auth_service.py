from __future__ import annotations

from flask import current_app
from itsdangerous import BadSignature, SignatureExpired, URLSafeTimedSerializer
from werkzeug.security import check_password_hash, generate_password_hash

from models.models import User, db

# Reset tokens are signed (no server-side storage) and valid for one hour.
RESET_TOKEN_MAX_AGE = 3600
_RESET_SALT = "password-reset"


def register_user(email: str, password: str) -> tuple[bool, str]:
    """
    Create a new user account after validating email uniqueness and password strength.
    Returns (success, message).
    """
    if User.query.filter_by(email=email).first():
        return False, "Cet e-mail est déjà utilisé."

    if not is_password_strong(password):
        return False, "Le mot de passe ne respecte pas les critères de sécurité."

    hashed_password = generate_password_hash(password, method="pbkdf2:sha256")
    new_user = User(email=email, password=hashed_password, role="user")
    db.session.add(new_user)
    db.session.commit()
    return True, "Inscription réussie ! Vous pouvez maintenant vous connecter."


def authenticate_user(email: str, password: str) -> User | None:
    """
    Verify credentials and return the user if valid, None otherwise.
    """
    user = User.query.filter_by(email=email).first()
    if user and check_password_hash(user.password, password):
        return user
    return None


def is_password_strong(password: str) -> bool:
    """
    Validate password strength:
    - At least 12 characters
    - At least one uppercase letter
    - At least one lowercase letter
    - At least one digit
    - At least one special character from @$!%*?&
    """
    return (
        len(password) >= 12
        and any(c.isupper() for c in password)
        and any(c.islower() for c in password)
        and any(c.isdigit() for c in password)
        and any(c in "@$!%*?&" for c in password)
    )


def _reset_serializer() -> URLSafeTimedSerializer:
    return URLSafeTimedSerializer(current_app.config["SECRET_KEY"], salt=_RESET_SALT)


def generate_reset_token(email: str) -> str:
    """Return a signed, time-limited token embedding the user's email."""
    return _reset_serializer().dumps(email)


def verify_reset_token(token: str, max_age: int = RESET_TOKEN_MAX_AGE) -> str | None:
    """Return the email if the token is valid and not expired, else None."""
    try:
        return _reset_serializer().loads(token, max_age=max_age)
    except (BadSignature, SignatureExpired):
        return None


def reset_password(email: str, new_password: str) -> tuple[bool, str]:
    """
    Update the user's password after validating its strength.
    Returns (success, message).
    """
    user = User.query.filter_by(email=email).first()
    if not user:
        return False, "Utilisateur introuvable."

    if not is_password_strong(new_password):
        return False, "Le mot de passe ne respecte pas les critères de sécurité."

    user.password = generate_password_hash(new_password, method="pbkdf2:sha256")
    db.session.commit()
    return True, "Mot de passe modifié avec succès !"
