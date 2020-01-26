# from flask import Flask
# from flask_sqlalchemy import SQLAlchemy
import sqlalchemy as db
from flask_sqlalchemy import declarative_base

# app = Flask(__name__)
# app.config["SQLALCHEMY_DATABASE_URI"] = "mysql://root:@Madaafhm7@localhost/world"
# app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
#
# db = SQLAlchemy(app)
#
#
# class City(db.Model):
#     __tablename__ = "city"
#     ID = db.Column(db.Integer, primary_key=True)
#     Name = db.Column(db.String(35), nullable=False)
#     CountryCode = db.Column(db.String(3), nullable=False)
#     District = db.Column(db.String(20), nullable=False)
#     Population = db.Column(db.Integer, nullable=False)
engine = db.create_engine('mysql+mysqlconnector://root:@Madaafhm7@localhost:3306/sqlalchemy_mysql')
connection = engine.connect()
results = engine.execute('SELECT * FROM posts LIMIT 10')
first = results.fetchone()
type(first)
type(first.items())
two = results.fetchmany(2)
all_ = results.fetchall()
type(all_)
query = 'SELECT * FROM posts'
# Classical Mapping example
from sqlalchemy import Table, MetaData, Column, Integer, String
from sqlalchemy.orm import mapper

metadata = MetaData()
tags = Table('Tags', metadata, Column('Id', Integer, primary_key=True),
             Column('Count', Integer), Column('ExcerptPostId', Integer),
             Column('Tagname', String(255)), Column('WikiPostId', Integer))


class Tags(object):
    def __init__(self, Count, ExcerptPostId, Tagname, WikiPostId):
        self.Count = Count
        self.ExcerptPostId = ExcerptPostId
        self.Tagname = Tagname
        self.WikiPostId = WikiPostId


tags_mapper = mapper(Tags, tags)
larger_tags = tags.select(Tags.Count > 1000)
engine.execute(larger_tags).fetchall()

#  quering with session based
from sqlalchemy.orm import sessionmaker

session = sessionmaker()
session.configure(bind=engine)
my_session = session()
my_session.query(Tags).first()
my_session.query(Tags).first().Tagname
my_session.query(Tags.Id, Tags.Tagname).first()
# querying with declarative base
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class Users(Base):
    __tablename__ = 'users'
    Id = Column(db.Integer, primary_key=True)
    Reputation = Column(db.Integer)
    CreationDate = Column(db.DateTime)
    DisplayName = Column(db.String(255))
    LastAccessDate = Column(db.DateTime)
    WebsiteUrl = Column(db.String(255))
    Location = Column(db.String(4096))
    AboutMe = Column(db.String(4096))
    Views = Column(db.Integer)
    UpVotes = Column(db.Integer)
    DownVotes = Column(db.Integer)
    AccountId = Column(db.Integer)

    def __repr__(self):
        return f'{self.__class__.__name__, self.Id, self.DisplayName}'


my_session.query(Users).first()  # ('Users', 0, 'Community') vs normal <__main__.Tags object at 0x000002C6F32859C8>
my_session.query(Users).first().DisplayName
for each_user in my_session.query(Users):
    print(each_user)

# see what query it is before executing
# method 1 - print
query = my_session.query(Users)
print(query)
# method 2 -echo
echo_engine = db.create_engine('mysql+mysqlconnector://root:@Madaafhm7@localhost:3306/sqlalchemy_mysql', echo=True)
echo_connection = echo_engine.connect()
echo_session = sessionmaker(bind=echo_engine)()
echo_session.query(Users).first()

# 2020-01-26 02:12:07,904 INFO sqlalchemy.engine.base.Engine BEGIN (implicit)
# 2020-01-26 02:12:07,905 INFO sqlalchemy.engine.base.Engine SELECT users.`Id` AS `users_Id`, users.`Reputation` AS `users_Reputation`, users.`CreationDate` AS `users_CreationDate`, users.`DisplayName` AS `users_DisplayName`, users.`LastAccessDate` AS `users_LastAccessDate`, users.`WebsiteUrl` AS `users_WebsiteUrl`, users.`Location` AS `users_Location`, users.`AboutMe` AS `users_AboutMe`, users.`Views` AS `users_Views`, users.`UpVotes` AS `users_UpVotes`, users.`DownVotes` AS `users_DownVotes`, users.`AccountId` AS `users_AccountId`
# FROM users
#  LIMIT %(param_1)s
# 2020-01-26 02:12:07,905 INFO sqlalchemy.engine.base.Engine {'param_1': 1}
# ('Users', 0, 'Community')

#  querying

echo_session.query(Users).filter_by(DisplayName='Community').all()
echo_session.query(Users).filter(Users.DisplayName == 'Community').all()
echo_session.query(Users.DisplayName).filter(Users.DisplayName.like('%Comm%')).all()
echo_session.query(Users.DisplayName).filter(Users.DisplayName.contains('Comm')).all()

# functions

from sqlalchemy import func

echo_session.query(func.sum(Tags.Count)).scalar()

# limit

echo_session.query(Users.DisplayName,
                   db.cast((Users.UpVotes - Users.DownVotes), db.Numeric(12, 2)).label('vote_difference'),
                   Users.UpVotes, Users.DownVotes).limit(10).all()

# order_by

echo_session.query(Users.DisplayName,
                   db.cast((Users.UpVotes - Users.DownVotes), db.Numeric(12, 2)).label('vote_difference'),
                   Users.UpVotes, Users.DownVotes).order_by('vote_difference').limit(10).all()

# desc

echo_session.query(Users.DisplayName,
                   db.cast((Users.UpVotes - Users.DownVotes), db.Numeric(12, 2)).label('vote_difference'),
                   Users.UpVotes, Users.DownVotes).order_by(db.desc('vote_difference')).limit(10).all()

# and, or , not, between

echo_session.query(Users.DisplayName).filter(Users.DisplayName == 'Community',
                                             Users.DownVotes.between(300, 600)).all()  # default is AND

echo_session.query(Users.DisplayName).filter(db.or_(Users.DisplayName == 'Community',
                                                    Users.DownVotes.between(300, 600))).all()


class Posts(Base):
    __tablename__ = "posts"
    Id = db.Column(db.Integer(), primary_key=True)
    Title = db.Column(db.String(255), nullable=False)
    ViewCount = db.Column(db.Integer(), default=1000)
    PostTypeId = db.Column(db.Integer(), default=True)
    OwnerUserId = db.Column(db.Integer())


# Joins

# Implicit Join

echo_session.query(Users, Posts).filter(Users.Id == Posts.OwnerUserId).first()

#  Explicit Join

echo_session.query(Users, Posts).join(Posts, Users.Id == Posts.OwnerUserId).first()


# Extend existing class

class Posts(Base):
    __tablename__ = "posts"
    Id = db.Column(db.Integer(), primary_key=True)
    Title = db.Column(db.String(255), nullable=False)
    ViewCount = db.Column(db.Integer(), default=1000)
    PostTypeId = db.Column(db.Integer(), default=True)
    OwnerUserId = db.Column(db.Integer())
    __table_args__ = {'extend_existing': True}
    AnswerCount = db.Column(db.Integer)
    ParentId = db.Column(db.Integer)
    Score = db.Column(db.Integer)

# Aliased Class


from sqlalchemy.orm import aliased
Questions = aliased(Posts)

# Self Join

echo_session.query(Posts.Id, Questions.Id, Posts.ViewCount, Posts.Score, Questions.Score).\
    filter(Posts.Id == Questions.ParentId).order_by(db.desc(Posts.ViewCount)).limit(10).all()

