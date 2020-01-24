from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.ext.automap import automap_base

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///C:\\Users\\Gautam\\database\\site.db'
db = SQLAlchemy(app)

users = db.Table('user', db.metadata, autoload=True, autoload_with=db.engine)
posts = db.Table('posts', db.metadata, autoload=True, autoload_with=db.engine)


@app.route('/')
def index():
    all_users = db.session.query(users).all()
    for user in all_users:
        print(user.username)
    all_posts = db.session.query(posts).all()
    for post in all_posts:
        print(post.title)
    return ''


if __name__ == '__main__':
    app.run(debug=True)
