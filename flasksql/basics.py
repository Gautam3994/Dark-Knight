from reflect_table import db
from flask_sqlalchemy import SQLAlchemy


class Example(db.Model):
    __tablename__ = 'sample'
    id = db.Column('id', db.Integer, primary_key=True)
    data = db.Column('data', db.Unicode)
    name = db.Column('name', db.String)
