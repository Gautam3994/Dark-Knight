import sqlalchemy as db
from sqlalchemy import MetaData

engine = db.create_engine('mysql+mysqlconnector://root:@Madaafhm7@localhost:3306/test_mysql', echo=True)
connection = engine.connect()

metadata = MetaData()

posts = db.Table('posts', metadata, db.Column('Id', db.Integer()),
                 db.Column('Title', db.String(255)),
                 db.Column('ViewCount', db.Integer()), db.Column('IsQuestion', db.Boolean()),
                 )
metadata.create_all(engine)

posts_new = db.Table('posts_new', metadata, db.Column('Id', db.Integer(), primary_key=True, unique=True),
                     db.Column('Title', db.String(255), nullable=False),
                     db.Column('ViewCount', db.Integer(), default=1000),
                     db.Column('IsQuestion', db.Boolean(), default=True),
                     )
posts_new.create(engine)

# The above constraint nullable doesnt work as per above code - Its normal

# creating using declarative base

engine = db.create_engine('sqlite:///sqlalchemy_sqlite.db', echo=True)
connection = engine.connect()

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()


class User(Base):
    __tablename__ = 'user'
    Id = db.Column(db.Integer(), primary_key=True)
    Name = db.Column(db.String())


# relationship

class Posts(Base):
    __tablename__ = 'posts'
    Id = db.Column(db.Integer(), primary_key=True)
    Title = db.Column(db.String(255), nullable=False)
    ViewCount = db.Column(db.Integer(), default=1000)
    Question = db.Column(db.Boolean(), default=True)
    OwnerUserId = db.Column(db.Integer(), db.schema.ForeignKey('user.Id'), nullable=False)
    User = relationship('User', backref='posts')


Base.metadata.create_all(engine)

#  inserting data

# Method 1

engine = db.create_engine('sqlite:///sqlalchemy_sqlite.db', echo=True)
connection = engine.connect()

metadata = MetaData()

users = db.Table('user', metadata, autoload=True, autoload_with=engine)
statement = db.insert(users).values(Name="Gautam")
result = connection.execute(statement)
result.rowcount

# Method 2

from sqlalchemy.orm import sessionmaker

session = sessionmaker()
session.configure(bind=engine)
my_session = session()

Devi = User(Name='Devi')
Kumar = User(Name='Kumar')
my_session.add(Devi)
my_session.add(Kumar)
my_session.new

#  IdentitySet([<__main__.User object at 0x000001ED6189CF48>, <__main__.User object at 0x000001ED60E1BAC8>]) - Results

my_session.commit()

for each_user in my_session.query(User).all():
    print(each_user.Name)

# Inserting mulitple values

posts = db.Table('posts', metadata, autoload=True, autoload_with=engine)
statement = db.insert(posts)
values_list = [{'Title': 'Data Science Question', 'OwnerUserId': 1},
               {'Title': 'Data  Question', 'OwnerUserId': 2}
               ]
result = connection.execute(statement, values_list)

# Inserting mulitple values - using classes

post_one = Posts(Title='Sample question', OwnerUserId=1)
post_two = Posts(Title="Sample Answer", Question=False, OwnerUserId=2)
my_session
my_session.add_all([post_one, post_two])
my_session.commit()
