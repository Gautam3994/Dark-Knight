from flask_blog import db, login_manager
from datetime import datetime
from flask_login import UserMixin


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), nullable=False, unique=True)
    email = db.Column(db.String(40), nullable=False, unique=True)
    profile_pciture = db.Column(db.String(20), nullable=False, default="default.jpg")
    password = db.Column(db.String(40), nullable=False)
    posts = db.relationship('Posts', backref='author', lazy=True)

    # backref - to mention col name in related Class(table) lazy to be able to fetch all
    # posts using the author

    def __repr__(self):
        return f"User('{self.username}', '{self.email}', '{self.id}')"


class Posts(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False, unique=True)
    posted_on = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    content = db.Column(db.Text, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def __repr__(self):
        return f"Posts('{self.title}', '{self.posted_on}')"
