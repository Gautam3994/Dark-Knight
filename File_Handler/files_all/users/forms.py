from flask_login import current_user
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, DateField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from files_all.models import User, FileContents


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


class FileForm(FlaskForm):
    _from = DateField(label='From', validators=[])
    to = DateField(label='To', validators=[])
    submit = SubmitField(label='Find')

    # TODO check there are records in this time and ensure end is after start date
    def validate_file_exists(self):
        user_id = current_user.id
        user_files = FileContents.query.filter_by(username=user_id).first()
        if not user_files:
            raise ValidationError("No files exist for this user")

    def validate(self, _from, to):
        if self.to <= self._from:
            raise ValidationError("To must be befor from")
