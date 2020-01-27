import os

from flask import Blueprint, request, render_template, url_for, current_app, flash
from flask_login import current_user, login_user, logout_user
from werkzeug.utils import redirect

from files_all import db, bcrypt
from files_all.models import FileContents, User
from files_all.users.forms import RegistrationForm, LoginForm


users = Blueprint('users', __name__)


@users.route("/")
def home():
    # page = request.args.get('page', default=1, type=int)
    # posts = FileContents.query.order_by(FileContents.desc()).paginate(page=page, per_page=4)
    # return render_template("home.html", posts=posts)
    return render_template("home.html")


@users.route("/register", methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('users.home'))
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data, email=form.email.data, password=hashed_password)
        db.session.add(user)
        db.session.commit()
        # path = os.path.join(current_app.root_path, 'static/files/', str(user.id))
        # os.mkdir(path)
        flash(f'Account was created successfully. You can log in now!', 'success')
        return redirect(url_for('users.login'))
    return render_template("register.html", title="Register", form=form)


@users.route("/login", methods=['GET', 'POST'])
def login():
    pass
    if current_user.is_authenticated:
        return redirect(url_for('users.home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user=user, remember=form.remember.data)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('users.home'))
        flash(f'Login failed. Please check email and password', 'danger')
    return render_template("login.html", title="Login", form=form)


@users.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('users.home'))


