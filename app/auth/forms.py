from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, SelectField
from wtforms.validators import DataRequired, Email, EqualTo, Length, ValidationError, Optional
from app.models import User


class LoginForm(FlaskForm):
    username = StringField("Username", validators=[DataRequired(), Length(min=3, max=64)])
    password = PasswordField("Password", validators=[DataRequired()])
    submit = SubmitField("Login")


class RegistrationForm(FlaskForm):
    username = StringField("Username", validators=[DataRequired(), Length(min=3, max=64)])
    email = StringField("Email", validators=[DataRequired(), Email(message="Bitte eine gültige E Mail Adresse eingeben."), Length(max=120)])
    password = PasswordField("Password", validators=[DataRequired(), Length(min=6, message="Passwort muss mindestens 6 Zeichen haben.")])
    password2 = PasswordField("Repeat Password", validators=[DataRequired(), EqualTo("password", message="Passwörter stimmen nicht überein.")])
    submit = SubmitField("Register")

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError("Username existiert bereits.")

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError("E Mail ist bereits registriert.")


class EditProfileForm(FlaskForm):
    username = StringField("Username", validators=[DataRequired(), Length(min=3, max=64)])
    email = StringField("Email", validators=[DataRequired(), Email(message="Bitte eine gültige E Mail Adresse eingeben."), Length(max=120)])
    submit = SubmitField("Save")

    def __init__(self, original_username, original_email, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.original_username = original_username
        self.original_email = original_email

    def validate_username(self, username):
        if username.data != self.original_username:
            user = User.query.filter_by(username=username.data).first()
            if user:
                raise ValidationError("Username existiert bereits.")

    def validate_email(self, email):
        if email.data != self.original_email:
            user = User.query.filter_by(email=email.data).first()
            if user:
                raise ValidationError("E Mail ist bereits registriert.")


class ChangePasswordForm(FlaskForm):
    current_password = PasswordField("Current Password", validators=[DataRequired()])
    new_password = PasswordField("New Password", validators=[DataRequired(), Length(min=6, message="Neues Passwort muss mindestens 6 Zeichen haben.")])
    new_password2 = PasswordField("Repeat New Password", validators=[DataRequired(), EqualTo("new_password", message="Passwörter stimmen nicht überein.")])
    submit = SubmitField("Change Password")


class AdminCreateUserForm(FlaskForm):
    username = StringField("Username", validators=[DataRequired(), Length(min=3, max=64)])
    email = StringField("Email", validators=[DataRequired(), Email(message="Bitte eine gültige E Mail Adresse eingeben."), Length(max=120)])
    role = SelectField("Role", choices=[("user", "User"), ("admin", "Admin")], validators=[DataRequired()])
    password = PasswordField("Password", validators=[DataRequired(), Length(min=6, message="Passwort muss mindestens 6 Zeichen haben.")])
    password2 = PasswordField("Repeat Password", validators=[DataRequired(), EqualTo("password", message="Passwörter stimmen nicht überein.")])
    submit = SubmitField("Create User")

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError("Username existiert bereits.")

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError("E Mail ist bereits registriert.")


class AdminEditUserForm(FlaskForm):
    email = StringField("Email", validators=[DataRequired(), Email(message="Bitte eine gültige E Mail Adresse eingeben."), Length(max=120)])
    role = SelectField("Role", choices=[("user", "User"), ("admin", "Admin")], validators=[DataRequired()])
    new_password = PasswordField("New Password (optional)", validators=[Optional(), Length(min=6, message="Neues Passwort muss mindestens 6 Zeichen haben.")])
    new_password2 = PasswordField("Repeat New Password", validators=[Optional(), EqualTo("new_password", message="Passwörter stimmen nicht überein.")])
    submit = SubmitField("Save")

    def __init__(self, original_email, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.original_email = original_email

    def validate_email(self, email):
        if email.data != self.original_email:
            user = User.query.filter_by(email=email.data).first()
            if user:
                raise ValidationError("E Mail ist bereits registriert.")
