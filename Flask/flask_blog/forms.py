from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, PasswordField, BooleanField, SubmitField, TextAreaField
from wtforms.validators import DataRequired, Email, EqualTo, Length, ValidationError
from flask_blog.models import User, Posts
from flask_login import current_user


class RegistrationForm(FlaskForm):
    username = StringField(label="Username", validators=[DataRequired(), Length(min=2, max=40, message="Username can be from 2 to 40 characters longs")])
    email = StringField(label="Email", validators=[DataRequired(), Email()])
    password = PasswordField(label="Password", validators=[DataRequired()])
    confirm_password = PasswordField(label="Confirm Passowrd", validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField(label='Sign Up')

    @staticmethod
    def validate_username(username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError("user name already exists")

    @staticmethod
    def validate_email(email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError("email already exists")


class LoginForm(FlaskForm):
    email = StringField(label="Email", validators=[DataRequired(), Email()])
    password = PasswordField(label="Password", validators=[DataRequired()])
    remember = BooleanField(label="remember me")
    submit = SubmitField(label='Login')


class UpdateAccountForm(FlaskForm):
    username = StringField(label="Username", validators=[DataRequired(), Length(min=2, max=40, message="Username can be from 2 to 40 characters longs")])
    profile_picture = FileField(label="Update Profile Picture", validators=[FileAllowed(['jpg', 'png'])])
    email = StringField(label="Email", validators=[DataRequired(), Email()])
    submit = SubmitField(label='Update')

    @staticmethod
    def validate_username(username):
        if username.data != current_user.username:
            user = User.query.filter_by(username=username.data).first()
            if user:
                raise ValidationError("user name already exists")

    @staticmethod
    def validate_email(email):
        if email.data != current_user.email:
            user = User.query.filter_by(email=email.data).first()
            if user:
                raise ValidationError("email already exists")


class PostForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])
    content = TextAreaField('Content', validators=[DataRequired()])
    file = FileField(label="Image", validators=[FileAllowed(['jpg', 'png'])])
    post = SubmitField(label='Post')


class RequestResetForm(FlaskForm):
    email = StringField(label="Email", validators=[DataRequired(), Email()])
    request_reset = SubmitField(label='Request Password Reset')

    @staticmethod
    def validate_email(email):
        user = User.query.filter_by(email=email.data).first()
        if user is None:
            raise ValidationError("This email is not associated with any account.")


class ResetPasswordForm(FlaskForm):
    password = PasswordField(label="Password", validators=[DataRequired()])
    confirm_password = PasswordField(label="Confirm Passowrd", validators=[DataRequired(), EqualTo('password')])
    reset_password = SubmitField(label="Reset Password")
