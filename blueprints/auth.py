"""Authentication and user account: login, register, profile, password reset."""

from flask import (
    Blueprint,
    current_app,
    flash,
    redirect,
    render_template,
    request,
    url_for,
)
from flask_login import current_user, login_required, login_user, logout_user
from flask_mail import Message
from werkzeug.security import check_password_hash, generate_password_hash

from extensions import limiter, mail
from models.models import User, db
from services.auth_service import authenticate_user, generate_reset_token, register_user
from services.auth_service import reset_password as do_reset_password
from services.auth_service import verify_reset_token

auth_bp = Blueprint("auth", __name__)


@auth_bp.route("/login", methods=["GET", "POST"])
@limiter.limit("10 per minute", methods=["POST"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for("auth.account"))

    if request.method == "POST":
        action = request.form.get("action")
        email = request.form.get("email")
        password = request.form.get("password")

        if action == "register":
            success, message = register_user(email, password)
            flash(message, "success" if success else "danger")
            return redirect(url_for("auth.login"))

        elif action == "login":
            user = authenticate_user(email, password)
            if user:
                login_user(user)
                next_page = request.args.get("next")
                return redirect(next_page or url_for("auth.account"))
            flash("Identifiants incorrects.", "danger")
            return redirect(url_for("auth.login"))

    return render_template("login.html")


@auth_bp.route("/account")
@login_required
def account():
    return render_template("account.html", user_name=current_user.email)


@auth_bp.route("/edit_profile", methods=["GET", "POST"])
@login_required
def edit_profile():
    """Let the user update their personal info (name, birth date, phone, email)."""
    user = User.query.get(current_user.user_id)

    if request.method == "POST":
        user.first_name = request.form.get("first_name")
        user.last_name = request.form.get("last_name")
        user.birth_date = request.form.get("birth_date") or None
        user.phone = request.form.get("phone")
        new_email = request.form.get("email")
        # Avoid duplicate email if the user changes it
        if new_email and new_email != user.email:
            if User.query.filter_by(email=new_email).first():
                flash("Cet email est déjà utilisé.", "danger")
                return redirect(url_for("auth.edit_profile"))
            user.email = new_email
        db.session.commit()
        flash("Profil mis à jour.", "success")
        return redirect(url_for("auth.account"))

    return render_template("edit_profile.html")


@auth_bp.route("/change_password", methods=["POST"])
@login_required
def change_password():
    """Handle password change from the edit_profile page."""
    user = User.query.get(current_user.user_id)
    current_pw = request.form.get("current_password")
    new_pw = request.form.get("new_password")
    confirm_pw = request.form.get("confirm_password")

    if not check_password_hash(user.password, current_pw):
        flash("Mot de passe actuel incorrect.", "danger")
        return redirect(url_for("auth.edit_profile"))

    if new_pw != confirm_pw:
        flash("Les mots de passe ne correspondent pas.", "danger")
        return redirect(url_for("auth.edit_profile"))

    if len(new_pw) < 12:
        flash("Le mot de passe doit contenir au moins 12 caractères.", "danger")
        return redirect(url_for("auth.edit_profile"))

    user.password = generate_password_hash(new_pw, method="pbkdf2:sha256")
    db.session.commit()
    flash("Mot de passe modifié avec succès.", "success")
    return redirect(url_for("auth.account"))


@auth_bp.route("/logout")
@login_required
def logout():
    logout_user()
    flash("Vous êtes déconnecté.", "success")
    return redirect(url_for("auth.login"))


def _send_password_reset_email(user):
    """Email a password-reset link to the given user."""
    token = generate_reset_token(user.email)
    reset_url = url_for("auth.reset_password", token=token, _external=True)
    msg = Message(
        "Réinitialisation de votre mot de passe Miaouff",
        recipients=[user.email],
    )
    msg.html = render_template(
        "emails/reset_password_email.html", user=user, reset_url=reset_url
    )
    mail.send(msg)


@auth_bp.route("/forgot_password", methods=["GET", "POST"])
@limiter.limit("5 per minute", methods=["POST"])
def forgot_password():
    """Public entry point: request a password-reset link by email."""
    if request.method == "POST":
        email = (request.form.get("email") or "").strip()
        user = User.query.filter_by(email=email).first()
        if user:
            try:
                _send_password_reset_email(user)
            except Exception as e:  # noqa: BLE001
                current_app.logger.warning("Reset email failed: %s", e)
        # Neutral message: never reveal whether an account exists for this email.
        flash(
            "Si un compte est associé à cette adresse, un lien de "
            "réinitialisation vient d'être envoyé.",
            "success",
        )
        return redirect(url_for("auth.login"))

    return render_template("forgot_password.html")


@auth_bp.route("/send_reset_code/<int:user_id>")
@limiter.limit("5 per minute")
def send_reset_code(user_id):
    """Admin action: send a reset link to a given user."""
    user = User.query.get(user_id)
    if not user:
        flash("Utilisateur introuvable.", "danger")
        return redirect(url_for("admin.edit_users"))
    try:
        _send_password_reset_email(user)
        flash("Le lien de réinitialisation a été envoyé par mail.", "success")
    except Exception as e:  # noqa: BLE001
        flash(f"Erreur lors de l'envoi du mail : {str(e)}", "danger")
    return redirect(url_for("admin.edit_users"))


@auth_bp.route("/reset_password/<token>", methods=["GET", "POST"])
@limiter.limit("10 per minute", methods=["POST"])
def reset_password(token):
    """Set a new password from a signed reset link."""
    email = verify_reset_token(token)
    if not email:
        flash("Lien de réinitialisation invalide ou expiré.", "danger")
        return redirect(url_for("auth.forgot_password"))

    if request.method == "POST":
        new_password = request.form.get("new_password")
        confirm = request.form.get("confirm_new_password")
        if new_password != confirm:
            flash("Les mots de passe ne correspondent pas.", "danger")
            return redirect(url_for("auth.reset_password", token=token))

        success, message = do_reset_password(email, new_password)
        flash(message, "success" if success else "danger")
        if success:
            return redirect(url_for("auth.login"))
        return redirect(url_for("auth.reset_password", token=token))

    return render_template("reset_password.html", token=token)
