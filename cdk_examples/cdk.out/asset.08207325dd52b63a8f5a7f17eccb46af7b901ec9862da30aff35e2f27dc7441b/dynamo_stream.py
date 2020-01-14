import json
import boto3
import os
sns_client = boto3.client('sns')


def handler(event, context):
    print(json.dumps(event))
    expected_price = os.environ['expected_price']
    if event["Records"][0]['eventName'] == 'MODIFY':
        if 'Price' in event["Records"][0]['dynamodb']['NewImage']:
            if int(event["Records"][0]['dynamodb']['NewImage']['Price']['N']) <= expected_price:
                product = event["Records"][0]['dynamodb']['NewImage']['product_id']['S']
                new_price = event["Records"][0]['dynamodb']['NewImage']['Price']['N']
                message = product + "price has dropped to " + new_price
