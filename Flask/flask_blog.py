from flask import Flask, render_template, url_for, flash, redirect
from forms import RegistrationForm, LoginForm
from datetime import datetime
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SECRET_KEY'] = 'cf8684c33f10290611a8a2616c40efcc'  # Got using secrets.token_hex(16) from secrets module
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
db = SQLAlchemy(app)


# after this import db in cmc
# then db.create_all() and then import User and Posts table and then use query


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), nullable=False, unique=True)
    email = db.Column(db.String(40), nullable=False, unique=True)
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


posts = [
    {
        "author": "Gautam Kumar",
        "title": "PUBG",
        "posted_on": "01-01-2020",
        "content": "About PUBG"
    },
    {
        "author": "Gautam",
        "title": "Cricket Article",
        "posted_on": "02-01-2020",
        "content": "About Cricket"
    }
]


@app.route("/")
@app.route("/home")
def home():
    return render_template("home.html", posts=posts)


@app.route("/about")
def about():
    return render_template("about.html", title="About")


@app.route("/register", methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        flash(f'Account was created successfully {form.username.data}', 'success')
        return redirect(url_for('home'))
    return render_template("register.html", title="Register", form=form)


@app.route("/login", methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        if form.email.data == 'a@b.com' and form.password.data == '123':
            flash(f'You have logged in successfully', 'success')
            return redirect(url_for('home'))
        else:
            flash(f'Login failed. Please check user name and password', 'danger')
    return render_template("login.html", title="Login", form=form)


if __name__ == '__main__':
    app.run(debug=True)
    # must set FLASK_APP=filename i.e flask_blog.py to use cmd(flask run)
    # Can use set FLASK_DEBUG=1 if you are using flask run
    # else can use python flask_blog.py
