import sqlalchemy as db
import pandas as pd

engine = db.create_engine('sqlite:///sqlalchemy_csv_1.db', echo=True)
connection = engine.connect()

with open('tags.csv', 'r') as file:
    tags_df = pd.read_csv(file)

tags_df.head()

#   Id           TagName  Count  ExcerptPostId  WikiPostId
# 0   1       definitions     22          105.0       104.0
# 1   2  machine-learning   3944         4909.0      4908.0
# 2   3           bigdata    329           66.0        65.0
# 3   5       data-mining    727           80.0        79.0
# 4   6         databases     55         8960.0      8959.0

tags_df.to_sql('tags', con=engine)

#  update

engine = db.create_engine('sqlite:///sqlalchemy_sqlite.db', echo=True)
connection = engine.connect()
engine.execute('select * from posts where Id=1').fetchone()
engine.execute('Update posts set ViewCount = 0 where Id= 1')

#  update method -2
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy.schema import ForeignKey
from sqlalchemy.orm import sessionmaker

session = sessionmaker()
session.configure(bind=engine)
my_session = session()
Base = declarative_base()


class User(Base):
    __tablename__ = 'user'
    Id = db.Column(db.Integer(), primary_key=True)
    Name = db.Column(db.String())


class Posts(Base):
    __tablename__ = 'posts'
    Id = db.Column(db.Integer(), primary_key=True)
    Title = db.Column(db.String(255), nullable=False)
    ViewCount = db.Column(db.Integer(), default=1000)
    Question = db.Column(db.Boolean(), default=True)
    OwnerUserId = db.Column(db.Integer(), db.schema.ForeignKey('user.Id'), nullable=False)
    User = relationship('User', backref='posts')


query = db.update(Posts).where(Posts.Id == 1).values(ViewCount=1)
result = connection.execute(query)
post_query = my_session.query(Posts).filter(Posts.Id == 1)
post_query.one().Id
post_query.one().ViewCount
post_query.one().Title

# updating mulitple records
query = db.update(Posts).values(ViewCount=Posts.ViewCount + 50)
result = connection.execute(query)

my_post = my_session.query(Posts).filter(Posts.Id == 1).one()
my_post.Title
my_post.Title = 'Modified'
my_session.dirty
my_session.commit()

# correlate updates
avg_views = db.select([db.func.avg(Posts.ViewCount).label("AverageViews")])
query = db.update(Posts).values(ViewCount=avg_views)
result = engine.execute(query)
result.rowcount


# delete

my_session.query(Posts.Id).all()
first_post = my_session.query(Posts).first()
first_post.Id
my_session.delete(first_post)
my_session.commit()

# deleting multiple records

my_session.query(Posts).filter(Posts.Id > 2).delete()

# important points in deleting tables

metadata = db.MetaData()
metadata.reflect(bind=engine)
metadata.tables.keys()
metadata.tables
post_table = metadata.tables['posts']
post_table.drop(bind=engine)