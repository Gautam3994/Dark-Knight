import json
import boto3
import pprint


def handler(event, context):
    pprint.pprint(event)
    product = event['pathParameters']['itemid']
    dynamodb_client = boto3.client('dynamodb')
    response = dynamodb_client.get_item(TableName="inventory", Key={
        'product_id': {'S': product}
    })
    if 'Item' in response:
        item = response["Item"]
    else:
        return result(400, 'item not found')
    # item['Price']['N'] = int(item['Price']['N'])
    return result(200, json.dumps(item))


def result(status, message):
    return {
        'statusCode': status,
        'body': message,
        'headers': {
            'Content-Type': 'application/json'
        }
    }


