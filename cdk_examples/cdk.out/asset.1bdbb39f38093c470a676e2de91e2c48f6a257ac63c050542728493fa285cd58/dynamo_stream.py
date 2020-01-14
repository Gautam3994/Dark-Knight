import json
import boto3
import os
sns_client = boto3.client('sns')


def handler(event, context):
    expected_price = os.environ['expected_price']
    sns_arn = os.environ['sns_arn']
    if event["Records"][0]['eventName'] == 'MODIFY':
        if 'Price' in event["Records"][0]['dynamodb']['NewImage']:
            if int(event["Records"][0]['dynamodb']['NewImage']['Price']['N']) <= int(expected_price):
                product = event["Records"][0]['dynamodb']['NewImage']['product_id']['S']
                new_price = event["Records"][0]['dynamodb']['NewImage']['Price']['N']
                message = product + "price has dropped to " + new_price
                sns_client.publish(TopicArn=sns_arn, Message=json.dumps({'default': json.dumps(message)}), MessageStructure='json')
