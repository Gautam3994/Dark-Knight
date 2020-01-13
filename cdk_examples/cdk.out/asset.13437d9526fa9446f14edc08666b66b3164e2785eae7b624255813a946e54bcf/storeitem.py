import boto3
import json
import pandas
from io import StringIO
session = boto3.Session(profile_name='dark_knight')
s3_client = session.client('s3')
dynamo = session.resource("dynamodb")
s3_resource = session.resource('s3')


def handler(event, context):
    print("Event" + json.dumps(event))
    inventory_bucket = event['Records'][0]['s3']['bucket']['name']
    inventory_bucket_key = event['Records'][0]['s3']['object']['key']
    object_ = s3_resource.Object(inventory_bucket, inventory_bucket_key)
    file_string = object_.get()['Body'].read().decode('utf-8')
    df = pandas.read_csv(StringIO(file_string))
    dicton = df.to_dict()
    print(dynamo.meta.client.list_tables())
    inventory_table = dynamo.Table('inventory')
    for i in range(len(dicton['Product'])):
        inventory_table.put_item(TableName='inventory', Item={
            'product_id': (dicton.get('Product', "None")[i]),
            'Transaction_date': (dicton.get('Transaction_date', "None")[i]),
            'Price': (dicton.get('Price', "None")[i]),
            'Payment_Type': (dicton.get('Payment_Type', "None")[i]),
            'Name': (dicton.get('Name', "None")[i]),
            'City': (dicton.get('City', "None")[i]),
            'State': (dicton.get('State', "None")[i]),
            'Country': (dicton.get('Country', "None")[i]),
            'Account_Created': (dicton.get('Account_Created', "None")[i]),
        })
