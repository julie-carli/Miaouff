"""Unit tests for the authentication service."""

from services.auth_service import (
    generate_reset_token,
    is_password_strong,
    verify_reset_token,
)


class TestPasswordStrength:
    def test_strong_password_is_accepted(self):
        assert is_password_strong("Password123!xyz") is True

    def test_too_short_is_rejected(self):
        assert is_password_strong("Ab1!") is False

    def test_missing_uppercase_is_rejected(self):
        assert is_password_strong("password123!") is False

    def test_missing_digit_is_rejected(self):
        assert is_password_strong("Password!!!!") is False

    def test_missing_special_char_is_rejected(self):
        assert is_password_strong("Password12345") is False


class TestResetToken:
    """Signed reset tokens (need the app context for the SECRET_KEY)."""

    def test_round_trip_returns_email(self, flask_app):
        with flask_app.app_context():
            token = generate_reset_token("alice@example.com")
            assert verify_reset_token(token) == "alice@example.com"

    def test_invalid_token_returns_none(self, flask_app):
        with flask_app.app_context():
            assert verify_reset_token("not-a-real-token") is None

    def test_expired_token_returns_none(self, flask_app):
        with flask_app.app_context():
            token = generate_reset_token("bob@example.com")
            # A negative max_age forces the token to be treated as expired.
            assert verify_reset_token(token, max_age=-1) is None
