from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_mail import Mail
from files_all.config import Config

db = SQLAlchemy()
bcrypt = Bcrypt()
login_manager = LoginManager()
login_manager.login_view = 'users.login'
login_manager.login_message_category = 'info'

mail = Mail()


# after this import db in cmc
# then db.create_all() and then import User and Posts table and then use query


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    with app.app_context():
        db.create_all(app=app)
    bcrypt.init_app(app)
    login_manager.init_app(app)
    mail.init_app(app)

    from files_all.users.routes import users

    app.register_blueprint(users)

    return app
