import os
import secrets

from flask import Blueprint, render_template, url_for, flash, request, abort, redirect, current_app
from flask_login import login_required, current_user


from flask_blog import db
from flask_blog.models import Posts
from flask_blog.posts.forms import PostForm

posts = Blueprint('posts', __name__)


@posts.route("/newpost", methods=['GET', 'POST'])
@login_required
def newpost():
    form = PostForm()
    if form.validate_on_submit():
        if form.file.data:
            hex_name = secrets.token_hex(8)
            _, file_ext = os.path.splitext(form.file.data.filename)
            file_name = hex_name + file_ext
            file_path = os.path.join(current_app.root_path, f'static/files/{str(current_user.id)}', file_name)
            form.file.data.save(file_path)
            current_user.posts.file = file_name
            post = Posts(title=form.title.data, content=form.content.data, author=current_user, file=file_name)
        else:
            post = Posts(title=form.title.data, content=form.content.data, author=current_user)
        db.session.add(post)
        db.session.commit()
        flash('Your post has been added successfully', 'success')
        return redirect(url_for('main.home'))
    return render_template("newpost.html", title="New Post", form=form, legend='Create Post')


@posts.route("/post/<int:post_id>")
def post(post_id):
    post = Posts.query.get_or_404(post_id)
    return render_template('post.html', title=post.title, post=post)


@posts.route("/post/<int:post_id>/update",  methods=['GET', 'POST'])
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
            file_path = os.path.join(current_app.root_path, f'static/files/{str(current_user.id)}', file_name)
            form.file.data.save(file_path)
            post.file = file_name
            # current_user.post.file = form.file.data.filename
        db.session.commit()
        flash("Your post was updated successfully", "success")
        return redirect(url_for('posts.post', post_id=post.id))
    elif request.method == 'GET':
        form.title.data = post.title
        form.content.data = post.content
        form.file.data = post.file
    return render_template("newpost.html", title="Update Post", form=form, legend='Update Post')


@posts.route("/post/<int:post_id>/delete",  methods=['POST'])
@login_required
def delete_post(post_id):
    post = Posts.query.get_or_404(post_id)
    if post.author != current_user:
        abort(403)
    db.session.delete(post)
    db.session.commit()
    flash('Your post has been deleted', 'success')
    return redirect(url_for('main.home'))
