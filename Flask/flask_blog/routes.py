from flask_blog.forms import RegistrationForm, LoginForm
from flask import render_template, url_for, flash, redirect
from flask_blog import app

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