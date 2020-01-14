import mongoengine
import datetime


class Owners(mongoengine.Document):
    registered_date = mongoengine.DateTimeField(default=datetime.datetime.now)
    name = mongoengine.StringField(required=True)
    email = mongoengine.EmailField(required=True)
    snake_ids = mongoengine.ListField()
    cage_ids = mongoengine.ListField()
    meta = {
        "alias": "core",
        "collection": "owners"
    }
