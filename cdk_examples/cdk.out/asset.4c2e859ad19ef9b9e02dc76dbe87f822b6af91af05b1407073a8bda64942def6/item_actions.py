import json
import boto3


def handler(event, context):
    dynamodb_client = boto3.client('dynamodb')
    product = event['pathParameters']['itemid']
    if event['httpMethod'] == 'GET':
        product = event['pathParameters']['itemid']
        response = dynamodb_client.get_item(TableName="inventory", Key={
            'product_id': {'S': product}
        })
        if 'Item' in response:
            item = response["Item"]
        else:
            return result(400, 'item not found')
    else:
        body_value = event['body']
        print(body_value)
        new_payment_type = body_value['Payment_Type']
        response = dynamodb_client.update_item(TableName='inventory', Key={'product_id': {'S': product}},
                                               UpdateExpression='SET #PT = :p',
                                               ExpressionAttributeNames={"#PT": "Payment_Type"},
                                               ExpressionAttributeValues={
                                                   ':p': {"S": str(new_payment_type)}
                                               },
                                               ReturnValues="ALL_NEW")
        if 'Attributes' in response:
            item = response['Attributes']
        else:
            return result(400, 'item not found')
    return result(200, json.dumps(item))


def result(status, message):
    return {
        'statusCode': status,
        'body': message,
        'headers': {
            'Content-Type': 'application/json'
        }
    }



