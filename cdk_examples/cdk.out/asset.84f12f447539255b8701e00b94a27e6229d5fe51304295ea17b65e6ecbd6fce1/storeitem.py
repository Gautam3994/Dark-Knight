import boto3
import json


def handler(event, context):
    print("This is {}".format(json.dump(event)))
