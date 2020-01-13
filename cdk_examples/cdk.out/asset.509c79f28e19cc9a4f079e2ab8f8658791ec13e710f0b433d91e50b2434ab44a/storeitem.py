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
    print(file)


event_ = {
    "Records": [
        {
            "eventVersion": "2.1",
            "eventSource": "aws:s3",
            "awsRegion": "us-east-2",
            "eventTime": "2019-12-28T19:28:46.584Z",
            "eventName": "ObjectCreated:Put",
            "userIdentity": {
                "principalId": "A3HHDPSP9902DW"
            },
            "requestParameters": {
                "sourceIPAddress": "49.207.131.195"
            },
            "responseElements": {
                "x-amz-request-id": "CC83944F473C8E34",
                "x-amz-id-2": "INDW05A8p60glZKcCF3ZgdM0IVW2/yrXhLrzLC73Loj92RdnyE0mooH0s3WycjWvdGEbvHOYIqk="
            },
            "s3": {
                "s3SchemaVersion": "1.0",
                "configurationId": "OWVhYjZmOGMtYWQzZi00OGQxLWJiYjItNTNhZDU2ZWIyMzE5",
                "bucket": {
                    "name": "inventorybucketdab03c52-caec-44af-853b-dfda5119958c",
                    "ownerIdentity": {
                        "principalId": "A3HHDPSP9902DW"
                    },
                    "arn": "arn:aws:s3:::inventorybucketdab03c52-caec-44af-853b-dfda5119958c"
                },
                "object": {
                    "key": "SalesJan2009.csv",
                    "size": 123637,
                    "eTag": "6392d2d39f31cfd7f888ae1f3c34c81b",
                    "versionId": "_op.cvbTFa.jqtcup10cPD0pXPAF9.62",
                    "sequencer": "005E07ACEE866FCC42"
                }
            }
        }
    ]
}

handler(event_, '')
