import os
import secrets
from PIL import Image

from flask import render_template, url_for, flash, redirect, request, abort
from flask_login import login_user, current_user, logout_user, login_required

from flask_blog import app, bcrypt, db
from flask_blog.forms import RegistrationForm, LoginForm, UpdateAccountForm, PostForm
from flask_blog.models import User, Posts


@app.route("/")
@app.route("/home")
def home():
    posts = Posts.query.all()
    return render_template("home.html", posts=posts)


@app.route("/about")
def about():
    return render_template("about.html", title="About")


@app.route("/register", methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data, email=form.email.data, password=hashed_password)
        db.session.add(user)
        db.session.commit()
        path = os.path.join(app.root_path, 'static/files/', str(user.id))
        os.mkdir(path)
        flash(f'Account was created successfully. You can log in now!', 'success')
        return redirect(url_for('login'))
    return render_template("register.html", title="Register", form=form)


@app.route("/login", methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user=user, remember=form.remember.data)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('home'))
        flash(f'Login failed. Please check email and password', 'danger')
    return render_template("login.html", title="Login", form=form)


@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('home'))


def upload_profile_picture(form_profile_picture):
    hex_name = secrets.token_hex(8)
    _, file_ext = os.path.splitext(form_profile_picture.filename)
    file_name = hex_name + file_ext
    file_path = os.path.join(app.root_path, 'static/profile_picture', file_name)
    required_size = (125, 125)
    resized_picture = Image.open(form_profile_picture)
    resized_picture.thumbnail(required_size)
    resized_picture.save(file_path)
    return file_name


@app.route("/account", methods=['GET', 'POST'])
@login_required
def account():
    form = UpdateAccountForm()
    if form.validate_on_submit():
        if form.profile_picture.data:
            new_profile_picture = upload_profile_picture(form.profile_picture.data)
            current_user.profile_picture = new_profile_picture
        current_user.username = form.username.data
        current_user.email = form.email.data
        db.session.commit()
        flash('Your account has been updated', 'success')
        return redirect(url_for('account'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.email.data = current_user.email
    profile_picture = url_for('static', filename="profile_picture/" + current_user.profile_picture)
    return render_template("account.html", title="Account", profile_picture=profile_picture, form=form)


@app.route("/newpost", methods=['GET', 'POST'])
@login_required
def newpost():
    form = PostForm()
    if form.validate_on_submit():
        if form.file.data:
            hex_name = secrets.token_hex(8)
            _, file_ext = os.path.splitext(form.file.data.filename)
            file_name = hex_name + file_ext
            file_path = os.path.join(app.root_path, f'static/files/{str(current_user.id)}', file_name)
            form.file.data.save(file_path)
            # current_user.posts.file = file_name
        if file_name:
            post = Posts(title=form.title.data, content=form.content.data, author=current_user, file=file_name)
        db.session.add(post)
        db.session.commit()
        flash('Your post has been added successfully', 'success')
        return redirect(url_for('home'))
    return render_template("newpost.html", title="New Post", form=form)


@app.route("/post/<int:post_id>")
def post(post_id):
    post = Posts.query.get_or_404(post_id)
    return render_template('post.html', title=post.title, post=post)


@app.route("/post/<int:post_id>/update")
@login_required
def update_post(post_id):
    post = Posts.query.get_or_404(post_id)
    if post.author != current_user:
        abort(403)
    form = PostForm()
    return render_template("newpost.html", title="Update Post", form=form)
