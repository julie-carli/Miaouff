"""Unit tests for the authentication service (no database needed)."""

import datetime

from services import auth_service
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
    def test_generated_token_validates(self):
        token = generate_reset_token("alice@example.com")
        assert verify_reset_token("alice@example.com", token) is True

    def test_wrong_token_is_rejected(self):
        generate_reset_token("bob@example.com")
        assert verify_reset_token("bob@example.com", "deadbeef") is False

    def test_empty_token_is_rejected(self):
        generate_reset_token("carol@example.com")
        assert verify_reset_token("carol@example.com", "") is False

    def test_unknown_email_is_rejected(self):
        assert verify_reset_token("nobody@example.com", "whatever") is False

    def test_expired_token_is_rejected(self):
        email = "dan@example.com"
        token = generate_reset_token(email)
        auth_service.reset_tokens[email][
            "expires_at"
        ] = datetime.datetime.utcnow() - datetime.timedelta(minutes=1)
        assert verify_reset_token(email, token) is False
