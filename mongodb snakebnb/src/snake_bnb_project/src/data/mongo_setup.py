import mongoengine


def setup():
    mongoengine.connect(alias='core', db="snake_bnb", host='localhost:27017')
