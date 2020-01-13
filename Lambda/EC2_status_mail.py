import boto3

client_mail = boto3.client('sns')


def lambda_handler(event, context):
    instance = event['detail']['instance-id']
    message = "This is my first lambda for EC2 {}".format(instance)
    email = client_mail.publish(
        TopicArn='arn:aws:sns:us-east-2:641484180035:Dark_Knight',
        Message=message,
        Subject='I will succeed not immediately but definetly'
    )