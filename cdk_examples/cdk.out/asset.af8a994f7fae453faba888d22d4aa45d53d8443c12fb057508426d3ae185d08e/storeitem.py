import boto3
import json
session = boto3.Session(profile_name='dark_knight')
s3_client = session.client('s3')
dynamo_client = session.client('dynamodb')
s3_resource = session.resource('s3')


def handler(event, context):
    print("Event" + json.dumps(event))
    inventory_bucket = event['Records'][0]['s3']['bucket']['name']
    inventory_bucket_key = event['Records'][0]['s3']['object']['key']
    object_ = s3_resource.Object(inventory_bucket, inventory_bucket_key)
    file = object_.get()['Body'].read().decode('utf-8')
