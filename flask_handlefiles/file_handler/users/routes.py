import bcrypt
from flask import render_template, request, url_for, flash
import os
from werkzeug import abort, redirect
from flask_login import login_required, current_user, login_user, logout_user
from file_handler.models import User, FileContents
from file_handler import app, db
from file_handler.users.forms import FileForm, RegistrationForm, LoginForm


@app.route('/')
def index():
    return render_template('index.html')


@app.route("/register", methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data, email=form.email.data, password=hashed_password)
        db.session.add(user)
        db.session.commit()
        flash(f'Account was created successfully. You can log in now!', 'success')
        return redirect(url_for('users.login'))
    return render_template("register.html", title="Register", form=form)


@app.route("/login", methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user=user, remember=form.remember.data)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('main.home'))
        flash(f'Login failed. Please check email and password', 'danger')
    return render_template("login.html", title="Login", form=form)


@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('main.home'))


@app.route('/upload', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        file = request.files['file']
        print(dir(file))
        file.save(os.path.join(app.config["UPLOAD_FOLDER"], file.filename))
        return file.filename


@app.route('/reports/<int:user_id>', methods=['GET', 'POST'])
@login_required
def view_reports(user_id):
    files = FileContents.query().filer(FileContents.user_id == user_id)
    if files.user_id != current_user.id:
        abort(403)
    form = FileForm
    if form.validate_on_submit():
        return "validated"
    else:
        return "not validated"

