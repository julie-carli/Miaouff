"""Send a real test email to confirm the SMTP configuration works.

Usage (with the MAIL_* environment variables set, e.g. via .env):
    python scripts/send_test_email.py [recipient]

Default recipient is neko.chan.levelup@gmail.com. Check that inbox afterwards.
"""

import sys

from flask_mail import Message

from app import app
from extensions import mail

DEFAULT_RECIPIENT = "neko.chan.levelup@gmail.com"


def main():
    recipient = sys.argv[1] if len(sys.argv) > 1 else DEFAULT_RECIPIENT
    with app.app_context():
        msg = Message(
            "Test d'envoi Miaouff",
            recipients=[recipient],
        )
        msg.body = (
            "Ceci est un e-mail de test envoyé par Miaouff.\n"
            "Si vous le recevez, la configuration SMTP fonctionne. 🐾"
        )
        sender = app.config.get("MAIL_DEFAULT_SENDER") or app.config.get(
            "MAIL_USERNAME"
        )
        print(f"Envoi depuis {sender} vers {recipient} ...")
        mail.send(msg)
        print("E-mail envoyé. Vérifiez la boîte de réception.")


if __name__ == "__main__":
    main()
