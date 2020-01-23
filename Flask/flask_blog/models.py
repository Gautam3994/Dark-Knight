from flask_blog import db, login_manager, app
from datetime import datetime
from flask_login import UserMixin
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), nullable=False, unique=True)
    email = db.Column(db.String(40), nullable=False, unique=True)
    profile_picture = db.Column(db.String(20), nullable=False, default="joker.jpg")
    password = db.Column(db.String(40), nullable=False)
    posts = db.relationship('Posts', backref='author', lazy=True)

    # backref - to mention col name in related Class(table) lazy to be able to fetch all
    # posts using the author

    def get_reset_token(self, expires_sec=300):
        serial = Serializer(app.config['SECRET_KEY'], expires_sec)
        return serial.dumps({'user_id': self.id}).decode('utf-8')

    @staticmethod
    def verify_reset_token(token):
        serial = Serializer(app.config['SECRET_KEY'])
        try:
            user_id = serial.loads(token)['user_id']
        except:
            return None
        return User.query.get(user_id)

    def __repr__(self):
        return f"User('{self.username}', '{self.email}', '{self.id}')"


class Posts(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    posted_on = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    file = db.Column(db.String)
    content = db.Column(db.Text, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def __repr__(self):
        return f"Posts('{self.title}', '{self.posted_on}')"
