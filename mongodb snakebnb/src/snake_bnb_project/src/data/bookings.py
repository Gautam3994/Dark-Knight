import mongoengine
import datetime


class Booking(mongoengine.EmbeddedDocument):
    guest_owner_id = mongoengine.ObjectIdField()
    guest_snake_id = mongoengine.ObjectIdField()
    booked_date = mongoengine.DateTimeField()
    check_in_date = mongoengine.DateTimeField(required=True)
    check_out_date = mongoengine.DateTimeField(required=True)
    rating = mongoengine.FloatField()
    review = mongoengine.StringField()

