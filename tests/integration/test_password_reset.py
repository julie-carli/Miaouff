"""Integration test for the password-reset email flow.

The SMTP send is mocked, so no real email is sent: the test only checks that a
message is composed with the right recipient and a working reset link. Real
inbox delivery is confirmed manually in prod (see scripts/send_test_email.py).
"""

from types import SimpleNamespace
from unittest.mock import patch

from blueprints.auth import _send_password_reset_email
from extensions import mail


def test_reset_email_is_sent_with_link(flask_app):
    user = SimpleNamespace(email="neko.chan.levelup@gmail.com", first_name="Neko")

    with flask_app.test_request_context():
        with patch.object(mail, "send") as mock_send:
            _send_password_reset_email(user)

    assert mock_send.call_count == 1
    message = mock_send.call_args[0][0]
    assert message.recipients == ["neko.chan.levelup@gmail.com"]
    # The email must carry a reset link to the token route.
    assert "/reset_password/" in message.html
    assert "Réinitialiser" in message.html
