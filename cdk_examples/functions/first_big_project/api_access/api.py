import json
import boto3
import decimal


class DecimalEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, decimal.Decimal):
            return float(o)
        return super(DecimalEncoder, self).default(o)


def handler(event, context):
    dynamo_client = boto3.client('dynamodb')
    response = dynamo_client.scan(TableName='inventory')
    response_json = {
        'statusCode': '200',
        'body': json.dumps(response, indent=2, cls=DecimalEncoder),
        'headers': {
            'Content-Type': 'application/json'
        }
    }
    return response_json
