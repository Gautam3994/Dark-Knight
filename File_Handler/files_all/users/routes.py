import os
import datetime
from flask import Blueprint, request, render_template, url_for, current_app, flash
from flask_login import current_user, login_user, logout_user, login_required
from werkzeug.utils import redirect, secure_filename

from files_all import db, bcrypt
from files_all.models import FileContents, User
from files_all.users.forms import RegistrationForm, LoginForm, NewFileForm, ViewFileForm
from sqlalchemy.sql import func

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


@users.route("/upload", methods=['GET', 'POST'])
@login_required
def upload():
    form = NewFileForm()
    if form.validate_on_submit():
        if form.upload.data:
            filename = secure_filename(form.upload.data.filename)
            filename_exist = FileContents.query.filter_by(file_name=filename).first()
            if filename_exist:
                flash("Please choose different filename", "warning")
            else:
                file_path = os.path.join(current_app.root_path, 'static/files/', filename)
                form.upload.data.save(file_path)
                file = FileContents(file_name=filename, author=current_user)
                db.session.add(file)
                db.session.commit()
                flash('Your file has been added successully', 'success')
                return redirect(url_for('users.home'))
    return render_template("uploadfile.html", title="Upload", form=form, legend='Upload File', isUpload=True)


@users.route("/allfiles", methods=['GET', 'POST'])
@login_required
def viewfiles():
    files = FileContents.query.all()
    return render_template("viewfiles.html", files=files, filesView=True)


@users.route("/yourfiles", methods=['GET', 'POST'])
@login_required
def viewyourfiles():
    yourfiles = FileContents.query.filter_by(author=current_user).all()
    # for file in yourfiles:
    #     print(type(datetime.datetime.date(file.uploaded_on)))
    if len(yourfiles) != 0:
        form = ViewFileForm()
        if form.start_date.data:
            if form.validate_on_submit(form.start_date, form.end_date):
                # SELECT * FROM file_contents WHERE date(uploaded_on) BETWEEN '2020-01-28' AND '2020-01-29';
                # selected_files = FileContents.query.filter(func.date(FileContents.uploaded_on).between(form.start_date.data, form.end_date.data)).filter_by(author=current_user).all()
                selected_files = []
                for file in yourfiles:
                    if form.end_date.data >= datetime.datetime.date(file.uploaded_on) >= form.start_date.data:
                        selected_files.append(file)
                # selected_files = [selected_files.append(file) for file in yourfiles if
                #                   form.end_date.data >= datetime.datetime.date(
                #                       file.uploaded_on) >= form.start_date.data]
                return render_template("yourfiles.html", form=form, files=selected_files, yourFile=True)
            else:
                flash("Check start and end date", "warning")
        return render_template("yourfiles.html", form=form, files=yourfiles, yourFile=True)
    else:
        flash('You dont have any files to display', 'warning')
        return redirect(url_for('users.viewfiles'))
    # if request.method == 'POST'

# return render_template("home.html")

# @users.route("/yourfiles", methods=['GET', 'POST'])
# @login_required
# def deletefiles():
