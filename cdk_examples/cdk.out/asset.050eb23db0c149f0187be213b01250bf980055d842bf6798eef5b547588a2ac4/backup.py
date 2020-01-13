import boto3
dynamo_client = boto3.client('dynamodb')


def handler(event, context):
    create_backup = dynamo_client.create_backup(TableName="inventory", BackupName="inventory_backup")
