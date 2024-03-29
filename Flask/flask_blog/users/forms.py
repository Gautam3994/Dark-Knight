from flask_login import current_user
from flask_wtf import FlaskForm
from flask_wtf.file import FileAllowed
from wtforms import StringField, PasswordField, SubmitField, BooleanField, FileField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError

from flask_blog.models import User


class RegistrationForm(FlaskForm):
    username = StringField(label="Username", validators=[DataRequired(), Length(min=2, max=40,
                                                                                message="Username can be from 2 to 40 characters longs")])
    email = StringField(label="Email", validators=[DataRequired(), Email()])
    password = PasswordField(label="Password", validators=[DataRequired()])
    confirm_password = PasswordField(label="Confirm Passowrd", validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField(label='Sign Up')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError("user name already exists")

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError("email already exists")


class LoginForm(FlaskForm):
    email = StringField(label="Email", validators=[DataRequired(), Email()])
    password = PasswordField(label="Password", validators=[DataRequired()])
    remember = BooleanField(label="remember me")
    submit = SubmitField(label='Login')


class UpdateAccountForm(FlaskForm):
    username = StringField(label="Username", validators=[DataRequired(), Length(min=2, max=40,
                                                                                message="Username can be from 2 to 40 characters longs")])
    profile_picture = FileField(label="Update Profile Picture", validators=[FileAllowed(['jpg', 'png'])])
    email = StringField(label="Email", validators=[DataRequired(), Email()])
    submit = SubmitField(label='Update')

    def validate_username(self, username):
        if username.data != current_user.username:
            user = User.query.filter_by(username=username.data).first()
            if user:
                raise ValidationError("user name already exists")

    def validate_email(self, email):
        if email.data != current_user.email:
            user = User.query.filter_by(email=email.data).first()
            if user:
                raise ValidationError("email already exists")


class RequestResetForm(FlaskForm):
    email = StringField(label="Email", validators=[DataRequired(), Email()])
    request_reset = SubmitField(label='Request Password Reset')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is None:
            raise ValidationError("This email is not associated with any account.")


class ResetPasswordForm(FlaskForm):
    password = PasswordField(label="Password", validators=[DataRequired()])
    confirm_password = PasswordField(label="Confirm Passowrd",
                                     validators=[DataRequired(), EqualTo('password')])
    reset_password = SubmitField(label="Reset Password")
