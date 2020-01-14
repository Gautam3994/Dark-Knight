from flask import Flask, render_template, url_for
app = Flask(__name__)

posts = [
    {
        "Author": "Gautam",
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
    return render_template("about.html", posts=posts, title="About")


if __name__ == '__main__':
    app.run(debug=True)
