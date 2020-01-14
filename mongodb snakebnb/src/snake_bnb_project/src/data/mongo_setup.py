import mongoengine


def setup():
    mongoengine.connect(db="mongo")
