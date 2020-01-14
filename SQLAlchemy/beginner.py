from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "mysql://root:@Madaafhm7@localhost/world"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)


class City(db.Model):
    __tablename__ = "city"
    ID = db.Column(db.Integer, primary_key=True)
    Name = db.Column(db.String(35), nullable=False)
    CountryCode = db.Column(db.String(3), nullable=False)
    District = db.Column(db.String(20), nullable=False)
    Population = db.Column(db.Integer, nullable=False)
