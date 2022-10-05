from wsgiref.validate import validator
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, EmailField, FileField
from flask_wtf.file import FileField, FileRequired, FileAllowed
from wtforms.validators import InputRequired, Length, EqualTo, ValidationError
from passlib.hash import pbkdf2_sha256

from model.models import User


def invalid_credentials(form, field):
    """Username and password checker"""
    email_entered = form.email.data
    password_entered = field.data
    user_object = User.query.filter_by(email=email_entered).first()
    if user_object is None:
        raise ValidationError("Email or password is incorrect")
    elif not pbkdf2_sha256.verify(password_entered, user_object.password):
        raise ValidationError("Email or password is incorrect")


class FindFriendForm(FlaskForm):
    """Find friends form"""

    friend_name = StringField(
        "friend_name_label",
        validators=[
            InputRequired(message="Friend name required"),
            Length(
                min=4,
                max=25,
                message="Friend name must be between 4 and 52 characters",
            ),
        ],
    )
    submit_button = SubmitField("Find")


class RegistrationForm(FlaskForm):
    """Registration form"""

    firstname = StringField(
        "first_label",
        validators=[
            InputRequired(message="First name required"),
            Length(
                min=4, max=25, message="First name must be between 4 and 25 characters"
            ),
        ],
    )
    lastname = StringField(
        "last_label",
        validators=[
            InputRequired(message="Last name required"),
            Length(
                min=4, max=25, message="Last name must be between 4 and 25 characters"
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
    email = StringField(
        "email_label",
        validators=[
            InputRequired(message="E-mail required"),
            Length(min=5, message="E-mail must be minimum 5 characters"),
        ],
    )
    picture_name = FileField(
        "profile_picture_label",
        validators=[FileAllowed(["jpg", "png"], "Images with type 'jpg' or 'png'.")],
    )
    submit_button = SubmitField("Continue to login and chat!")


    def validate_email(self, email):
        user_object = User.query.filter_by(email=email.data).first()
        if user_object:
            raise ValidationError("Email already exists. Select a different email.")


class LoginForm(FlaskForm):
    """Login form"""

    email = StringField(
        "email_label",
        validators=[
            InputRequired(message="E-mail required"),
        ],
    )
    password = PasswordField(
        "password_label",
        validators=[InputRequired(message="Password  requaired"), invalid_credentials],
    )

    submit_button = SubmitField("Login")
