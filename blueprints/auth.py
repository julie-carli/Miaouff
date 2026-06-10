"""Authentication and user account: login, register, profile, password reset."""

from flask import Blueprint, flash, redirect, render_template, request, url_for
from flask_login import current_user, login_required, login_user, logout_user
from flask_mail import Message
from werkzeug.security import check_password_hash, generate_password_hash

from extensions import mail
from models.models import User, db
from services.auth_service import authenticate_user, generate_reset_token, register_user
from services.auth_service import reset_password as do_reset_password
from services.auth_service import verify_reset_token

auth_bp = Blueprint("auth", __name__)


@auth_bp.route("/login", methods=["GET", "POST"])
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


@auth_bp.route("/send_reset_code/<int:user_id>")
def send_reset_code(user_id):
    user = User.query.get(user_id)
    if not user:
        flash("Utilisateur introuvable.", "danger")
        return redirect(url_for("admin.edit_users"))

    reset_code = generate_reset_token(user.email)
    msg = Message("Réinitialisation de votre mot de passe", recipients=[user.email])
    msg.html = f"""
    <html>
        <body>
            <h2 style="color: #4CAF50;">Réinitialisation de votre mot de passe</h2>
            <p>Bonjour {user.first_name} {user.last_name},</p>
            <p>Veuillez utiliser le code suivant pour réinitialiser votre mot de passe :</p>
            <h3 style="background-color: #f4f4f4; padding: 10px; border-radius: 5px; color: #333;">
                {reset_code}
            </h3>
            <p>Si vous n'avez pas demandé cette réinitialisation, ignorez cet e-mail.</p>
            <p>Cordialement,<br>L'équipe Miaouff</p>
        </body>
    </html>
    """
    try:
        mail.send(msg)
        flash("Le code a été envoyé par mail.", "success")
    except Exception as e:
        flash(f"Erreur lors de l'envoi du mail : {str(e)}", "danger")

    return redirect(url_for("admin.edit_users"))


@auth_bp.route("/reset_password", methods=["GET", "POST"])
def reset_password():
    if request.method == "POST":
        email = request.form.get("email")
        code = request.form.get("code")
        new_password = request.form.get("new_password")

        if not verify_reset_token(email, code):
            flash("Code invalide.", "danger")
            return redirect(url_for("auth.reset_password"))

        success, message = do_reset_password(email, new_password)
        flash(message, "success" if success else "danger")
        if success:
            return redirect(url_for("auth.login"))

    return render_template("reset_password.html")
