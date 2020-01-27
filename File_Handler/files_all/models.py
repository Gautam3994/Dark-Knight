from datetime import datetime
from flask_login import UserMixin

from files_all import login_manager, db


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), nullable=False, unique=True)
    email = db.Column(db.String(40), nullable=False, unique=True)
    password = db.Column(db.String(40), nullable=False)
    files = db.relationship('FileContents', backref='author', lazy=True)


class FileContents(db.Model):
    id = db.Column(db.Integer, primary_key=True, unique=True)
    file_name = db.Column(db.String(300))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    uploaded_on = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    def __repr__(self):
        return f"Posts('{self.file_name}', '{self.uploaded_on}', {self.user_id})"
