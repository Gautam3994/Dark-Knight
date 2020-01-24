from flask import Blueprint, request, render_template

from flask_blog.models import Posts

main = Blueprint('main', __name__)


@main.route("/")
@main.route("/home")
def home():
    page = request.args.get('page', default=1, type=int)
    posts = Posts.query.order_by(Posts.posted_on.desc()).paginate(page=page, per_page=4)
    return render_template("home.html", posts=posts)


@main.route("/about")
def about():
    return render_template("about.html", title="About")
