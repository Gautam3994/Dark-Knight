import json
import random
from faker import Faker

fake = Faker()


def handler(event, context):
    item = {}
    print(json.dumps(event))
    item['order_id'] = event['order_id']
    item['name'] = get_item_name()
    item['receiptient'] = get_receiptient()
    item['price'] = get_item_price()
    item['shipping_address'] = get_shipping_address()
    item['delivery_status'] = get_delivery_status()
    item['expected_delivery_date'] = get_delivery_date()
    print(item)
    response_json = {
        'statusCode': '200',
        'body': json.dumps(item, indent=2),
        'headers': {
            'Content-Type': 'application/json'
        }
    }
    return response_json


def get_item_name():
    return fake.word()


def get_item_price():
    return random.randint(100, 3000)


def get_shipping_address():
    return fake.address()


def get_delivery_status():
    status = ["shipped", "out for delivery", "delivered", "processing order"]
    return random.choice(status)


def get_delivery_date():
    return fake.date()


def get_receiptient():
    return fake.name()


