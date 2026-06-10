import secrets
from datetime import datetime, timedelta

from werkzeug.security import check_password_hash, generate_password_hash

from models.models import User, db

# In-memory store for password-reset codes: email -> {"token", "expires_at"}.
# Note: should be replaced by a DB table in production so codes survive restarts.
reset_tokens = {}

# Reset codes are valid for a limited time only.
RESET_TOKEN_TTL = timedelta(minutes=15)


def register_user(email, password):
    """
    Create a new user account after validating email uniqueness and password strength.
    Returns (success: bool, message: str).
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


def authenticate_user(email, password):
    """
    Verify credentials and return the user if valid, None otherwise.
    """
    user = User.query.filter_by(email=email).first()
    if user and check_password_hash(user.password, password):
        return user
    return None


def is_password_strong(password):
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


def generate_reset_token(email):
    """
    Generate and store a time-limited reset token for the given email.
    Returns the generated token.
    """
    token = secrets.token_hex(4)
    reset_tokens[email] = {
        "token": token,
        "expires_at": datetime.utcnow() + RESET_TOKEN_TTL,
    }
    return token


def verify_reset_token(email, code):
    """
    Check that the provided code matches the stored token and is not expired.
    Uses a constant-time comparison to avoid timing attacks.
    """
    entry = reset_tokens.get(email)
    if not entry:
        return False
    if datetime.utcnow() > entry["expires_at"]:
        reset_tokens.pop(email, None)
        return False
    return secrets.compare_digest(entry["token"], code or "")


def reset_password(email, new_password):
    """
    Update the user's password and remove the used reset token (single use).
    Returns (success: bool, message: str).
    """
    user = User.query.filter_by(email=email).first()
    if not user:
        return False, "Utilisateur introuvable."

    if not is_password_strong(new_password):
        return False, "Le mot de passe ne respecte pas les critères de sécurité."

    user.password = generate_password_hash(new_password, method="pbkdf2:sha256")
    db.session.commit()
    reset_tokens.pop(email, None)
    return True, "Mot de passe modifié avec succès !"
