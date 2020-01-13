import boto3
import logging
dynamo_client = boto3.client('dynamodb')
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


def handler(event, context):
    logger.info(f"Function: {context.function_name} has started to run")
    create_backup = dynamo_client.create_backup(TableName="inventory", BackupName="inventory_backup")
