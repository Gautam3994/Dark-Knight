import boto3
sfn_client = boto3.client("stepfunctions")


def handler(event, context):
    response = sfn_client.start_execution(stateMachineArn="arn:aws:states:us-east-2:641484180035:stateMachine:simplestatemachine")
