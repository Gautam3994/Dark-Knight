import os
import secrets
from PIL import Image

from flask import render_template, url_for, flash, redirect, request, abort
from flask_login import login_user, current_user, logout_user, login_required

from flask_blog import app, bcrypt, db
from flask_blog.forms import (RegistrationForm, LoginForm, UpdateAccountForm,
                              PostForm, RequestResetForm, ResetPasswordForm)
from flask_blog.models import User, Posts


@app.route("/")
@app.route("/home")
def home():
    page = request.args.get('page', default=1, type=int)
    posts = Posts.query.order_by(Posts.posted_on.desc()).paginate(page=page, per_page=4)
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
            current_user.posts.file = file_name
            post = Posts(title=form.title.data, content=form.content.data, author=current_user, file=file_name)
        else:
            post = Posts(title=form.title.data, content=form.content.data, author=current_user)
        db.session.add(post)
        db.session.commit()
        flash('Your post has been added successfully', 'success')
        return redirect(url_for('home'))
    return render_template("newpost.html", title="New Post", form=form, legend='Create Post')


@app.route("/post/<int:post_id>")
def post(post_id):
    post = Posts.query.get_or_404(post_id)
    return render_template('post.html', title=post.title, post=post)


@app.route("/post/<int:post_id>/update",  methods=['GET', 'POST'])
@login_required
def update_post(post_id):
    post = Posts.query.get_or_404(post_id)
    if post.author != current_user:
        abort(403)
    form = PostForm()
    if form.validate_on_submit():
        post.title = form.title.data
        post.content = form.content.data
        if form.file.data:
            hex_name = secrets.token_hex(8)
            _, file_ext = os.path.splitext(form.file.data.filename)
            file_name = hex_name + file_ext
            file_path = os.path.join(app.root_path, f'static/files/{str(current_user.id)}', file_name)
            form.file.data.save(file_path)
            post.file = file_name
            # current_user.post.file = form.file.data.filename
        db.session.commit()
        flash("Your post was updated successfully", "success")
        return redirect(url_for('post', post_id=post.id))
    elif request.method == 'GET':
        form.title.data = post.title
        form.content.data = post.content
        form.file.data = post.file
    return render_template("newpost.html", title="Update Post", form=form, legend='Update Post')


@app.route("/post/<int:post_id>/delete",  methods=['POST'])
@login_required
def delete_post(post_id):
    post = Posts.query.get_or_404(post_id)
    if post.author != current_user:
        abort(403)
    db.session.delete(post)
    db.session.commit()
    flash('Your post has been deleted', 'success')
    return redirect(url_for('home'))


@app.route("/user/<string:username>")
def user_posts(username):
    page = request.args.get('page', default=1, type=int)
    user = User.query.filter_by(username=username).first_or_404()
    posts = Posts.query.filter_by(author=user).order_by(Posts.posted_on.desc()).paginate(page=page, per_page=4)
    return render_template("user_posts.html", posts=posts, user=user)


def send_reset_email(email):
    pass


@app.route("/reset_password", methods=['GET', 'POST'])
def reset_request():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = RequestResetForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        send_reset_email(user.email)
        flash("The email has been sent to your email id", "info")
        return redirect(url_for('login'))
    return render_template("reset_request.html", title="Reset Password", form=form)


@app.route("/reset_password/<token>", methods=['GET', 'POST'])
def reset_token(token):
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    user = User.verify_reset_token(token)
    if not user:
        flash("That is an invalid or expired token", "warning")
        return redirect(url_for("reset_request"))
    form = ResetPasswordForm()
    return render_template("reset_token.html", title="Reset Password", form=form)
