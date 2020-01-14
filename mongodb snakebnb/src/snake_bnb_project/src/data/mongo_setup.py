import mongoengine


def setup():
    mongoengine.register_connection(alias='core', db="snake_bnb_mongo")