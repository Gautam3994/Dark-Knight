import boto3
import json


def handler(event, context):
    print("Event" + json.dumps(event))
