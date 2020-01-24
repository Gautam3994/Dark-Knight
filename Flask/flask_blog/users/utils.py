import os
import secrets

from PIL import Image
from flask_mail import Message

from flask_blog import mail, app

from flask import url_for


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


def send_reset_email(user):
    token = user.get_reset_token()
    msg = Message('Password Reset', sender=os.environ.get('EMAIL'), recipients=[user.email])
    msg.body = f'''To reset your password, click the following link
{ url_for('reset_token', token=token, _external=True)}
'''
    mail.send(msg)
