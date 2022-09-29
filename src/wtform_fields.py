from wsgiref.validate import validator
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, EmailField, FileField
from flask_wtf.file import FileField, FileRequired, FileAllowed
from wtforms.validators import InputRequired, Length, EqualTo, ValidationError
from passlib.hash import pbkdf2_sha256

from model.models import User


def invalid_credentials(form, field):
    """Username and password checker"""
    username_entered = form.username.data
    password_entered = field.data
    user_object = User.query.filter_by(username=username_entered).first()
    if user_object is None:
        raise ValidationError("Username or password is incorrect")
    elif not pbkdf2_sha256.verify(password_entered, user_object.password):
        raise ValidationError("Username or password is incorrect")


class FindFriendForm(FlaskForm):
    """Find friends form"""

    friend_username = StringField(
        "friend_username_label",
        validators=[
            InputRequired(message="Friend username required"),
            Length(
                min=4,
                max=25,
                message="Friend username must be between 4 and 25 characters",
            ),
        ],
    )
    submit_button = SubmitField("Find")


class RegistrationForm(FlaskForm):
    """Registration form"""

    username = StringField(
        "username_label",
        validators=[
            InputRequired(message="Username required"),
            Length(
                min=4, max=25, message="Username must be between 4 and 25 characters"
            ),
        ],
    )
    password = PasswordField(
        "password_label",
        validators=[
            InputRequired(message="Password required"),
            Length(
                min=4, max=25, message="Passowrd must be between 4 and 25 characters"
            ),
        ],
    )
    confirm_password = PasswordField(
        "confirm_password_label",
        validators=[
            InputRequired(message="Passowrd required"),
            EqualTo("password", message="Passwords must match"),
        ],
    )
    email = StringField(
        "email_label",
        validators=[
            InputRequired(message="E-mail required"),
            Length(min=5, message="E-mail must be minimum 5 characters"),
        ],
    )
    profile_picture = FileField(
        "profile_picture_label",
        validators=[FileAllowed(["jpg", "png"], "Images with type 'jpg' or 'png'.")],
    )
    submit_button = SubmitField("Create")

    def validate_username(self, username):
        user_object = User.query.filter_by(username=username.data).first()
        if user_object:
            raise ValidationError(
                "Username already exists. Select a different username."
            )

    def validate_email(self, email):
        user_object = User.query.filter_by(email=email.data).first()
        if user_object:
            raise ValidationError("Email already exists. Select a different email.")


class LoginForm(FlaskForm):
    """Login form"""

    username = StringField(
        "username_label",
        validators=[InputRequired(message="Username requaired.")],
    )
    password = PasswordField(
        "password_label",
        validators=[InputRequired(message="Password  requaired"), invalid_credentials],
    )
    submit_button = SubmitField("Login")
