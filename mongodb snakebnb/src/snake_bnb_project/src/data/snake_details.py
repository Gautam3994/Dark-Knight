import mongoengine
import datetime


class Snake(mongoengine.Document):
    name = mongoengine.StringField(required=True)
    registered_date = mongoengine.DateTimeField(default=datetime.datetime.now)
    length = mongoengine.FloatField()
    is_venomous = mongoengine.BooleanField()
    species = mongoengine.StringField()
    meta = {
        "alias": "core",
        "collection": "snakes"
    }
