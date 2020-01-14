from flask_sqlalchemy import SQLAlchemy
from flask import Flask
import json
from settings import app

db = SQLAlchemy(app)


class Table(db.Model):
    __tablename__ = 'posts'
    id = db.Column(db.Integer, primarykey=True)
    Author = db.Column(db.String(100), nullable=False)
    Title = db.Column(db.String(200), nullable=False, unique=True)
    posted_on = db.Column(db.String(30), nullable=False)
    Content = db.Column(db.String, nullable=False)

