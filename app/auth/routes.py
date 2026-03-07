from flask import Blueprint, render_template, redirect, url_for, flash
from flask_login import login_user, logout_user, login_required, current_user
from functools import wraps
from app.models import User
from app.auth.forms import (
    LoginForm, RegistrationForm, EditProfileForm, ChangePasswordForm,
    AdminCreateUserForm, AdminEditUserForm
)
from app import db

auth = Blueprint("auth", __name__, url_prefix="/auth")


def admin_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if not current_user.is_authenticated or current_user.role != "admin":
            flash("Admin access required.")
            return redirect(url_for("assets.dashboard"))
        return f(*args, **kwargs)
    return decorated


@auth.route("/login", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for("assets.dashboard"))

    form = LoginForm()

    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()

        if user and user.check_password(form.password.data):
            login_user(user)
            return redirect(url_for("assets.dashboard"))

        flash("Invalid username or password")

    return render_template("auth/login.html", form=form)


@auth.route("/register", methods=["GET", "POST"])
def register():
    if current_user.is_authenticated:
        return redirect(url_for("assets.dashboard"))

    form = RegistrationForm()

    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data, role="user")
        user.set_password(form.password.data)

        db.session.add(user)
        db.session.commit()

        flash("Registration successful. Please login.")
        return redirect(url_for("auth.login"))

    return render_template("auth/register.html", form=form)


@auth.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("auth.login"))


@auth.route("/profile")
@login_required
def profile():
    return render_template("profile.html", user=current_user)


@auth.route("/profile/edit", methods=["GET", "POST"])
@login_required
def edit_profile():
    form = EditProfileForm(original_username=current_user.username, original_email=current_user.email)

    if form.validate_on_submit():
        current_user.username = form.username.data
        current_user.email = form.email.data
        db.session.commit()
        flash("Profile updated.")
        return redirect(url_for("auth.profile"))

    if form.username.data is None:
        form.username.data = current_user.username
    if form.email.data is None:
        form.email.data = current_user.email

    return render_template("profile_edit.html", form=form)


@auth.route("/profile/password", methods=["GET", "POST"])
@login_required
def change_password():
    form = ChangePasswordForm()

    if form.validate_on_submit():
        if not current_user.check_password(form.current_password.data):
            flash("Current password is incorrect.")
            return render_template("profile_password.html", form=form)

        current_user.set_password(form.new_password.data)
        db.session.commit()
        flash("Password updated successfully.")
        return redirect(url_for("auth.profile"))

    return render_template("profile_password.html", form=form)


# -------------------------
# Admin: User Management
# -------------------------

@auth.route("/admin/users")
@login_required
@admin_required
def admin_users():
    users = User.query.order_by(User.id.asc()).all()
    return render_template("admin/users.html", users=users)


@auth.route("/admin/users/create", methods=["GET", "POST"])
@login_required
@admin_required
def admin_create_user():
    form = AdminCreateUserForm()

    if form.validate_on_submit():
        user = User(
            username=form.username.data,
            email=form.email.data,
            role=form.role.data
        )
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash("User created.")
        return redirect(url_for("auth.admin_users"))

    return render_template("admin/user_form.html", form=form, mode="create")


@auth.route("/admin/users/<int:id>/edit", methods=["GET", "POST"])
@login_required
@admin_required
def admin_edit_user(id):
    user = db.session.get(User, id)
    if not user:
        flash("User not found.")
        return redirect(url_for("auth.admin_users"))

    form = AdminEditUserForm(original_email=user.email)

    if form.validate_on_submit():
        user.email = form.email.data
        user.role = form.role.data

        if form.new_password.data:
            user.set_password(form.new_password.data)

        db.session.commit()
        flash("User updated.")
        return redirect(url_for("auth.admin_users"))

    if form.email.data is None:
        form.email.data = user.email
    if form.role.data is None:
        form.role.data = user.role

    return render_template("admin/user_form.html", form=form, mode="edit", user=user)
