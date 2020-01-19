from flask import Flask, render_template, url_for, flash, redirect
from forms import RegistrationForm, LoginForm

app = Flask(__name__)
app.config['SECRET_KEY'] = 'cf8684c33f10290611a8a2616c40efcc'  # Got using secrets.token_hex(16) from secrets module
posts = [
    {
        "Author": "Gautam Kumar",
        "Title": "PUBG",
        "posted_on": "01-01-2020",
        "Content": "About PUBG"
    },
    {
        "Author": "Gautam",
        "Title": "Cricket Article",
        "posted_on": "02-01-2020",
        "Content": "About Cricket"
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


@app.route("/login")
def login():
    form = LoginForm()
    return render_template("login.html", title="Login", form=form)


if __name__ == '__main__':
    app.run(debug=True)
    # must set FLASK_APP=filename i.e flask_blog.py to use cmd(flask run)
    # Can use set FLASK_DEBUG=1 if you are using flask run
    # else can use python flask_blog.py
