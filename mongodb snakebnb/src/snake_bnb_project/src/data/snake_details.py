import mongoengine
import datetime


class Snake(mongoengine.Document):
    name = mongoengine.StringField(required=True)
    registered_date = mongoengine.DateTimeField(default=datetime.datetime.now)
    register_id = mongoengine.IntField(required=True)
    length = mongoengine.FloatField(required=True)
    is_venomous = mongoengine.BooleanField(required=True)
    species = mongoengine.StringField(required=True)
    meta = {
        "alias": "core",
        "collection": "snakes"
    }
