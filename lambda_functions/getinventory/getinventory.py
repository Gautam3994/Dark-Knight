import json
from faker import Faker
import random
import string
fake = Faker()


def handler(event, context):
    inventory = []
    for any_value in range(2):
        shoe = {}
        shoe_type = get_shoetype()
        shoe['type'] = shoe_type
        shoe['name'] = get_shoename(shoe_type)
        shoe['colour'] = get_shoecolour()
        shoe['description'] = get_shoe_description()
        shoe['warranty_period'] = get_warrant_period()
        shoe['model_number'] = get_model_number()
        inventory.append(shoe)
    response_json = {
        'statusCode': '200',
        'body': json.dumps(inventory, indent=2),
        'headers': {
            'Content-Type': 'application/json'
        }
    }
    return response_json


def get_shoetype():
    shoetypes = ["High Top", 'Mid Top', 'Casual shoes', "Formal shoes", "School shoes", "Trekking shoes"]
    return random.choice(shoetypes)


def get_shoecolour():
    shoecolor = ["Black", "Blue", "Green", "White", "Grey"]
    return random.choice(shoecolor)


def get_shoename(type_):
    return fake.sentence() + " " + type_


def get_warrant_period():
    return random.randint(1, 3)


def get_model_number():
    return "".join(random.choices((string.ascii_letters + string.digits), k=8))


def get_shoe_description():
    return fake.text()


handler("", "")
