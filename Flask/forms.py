from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired, Email, EqualTo, Length


class RegistrationForm(FlaskForm):
    username = StringField(label="Username", validators=[DataRequired(), Length(min=2, max=40, message="Username can be from 2 to 40 characters longs")])
    email = StringField(label="Email", validators=[DataRequired(), Email()])
    password = PasswordField(label="Password", validators=[DataRequired()])
    confirm_password = PasswordField(label="Confirm Passowrd", validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField(label='Sign Up')


class LoginForm(FlaskForm):
    email = StringField(label="Email", validators=[DataRequired(), Email()])
    password = PasswordField(label="Password", validators=[DataRequired()])
    remember = BooleanField(label="remember me")
    submit = SubmitField(label='Login')

