import json
import boto3
import pprint

# session = boto3.Session(profile_name='dark_knight')
# event_1 = {
#     "resource": "/items/{itemid}",
#     "path": "/items/Gautam",
#     "httpMethod": "PUT",
#     "headers": None,
#     "multiValueHeaders": None,
#     "queryStringParameters": None,
#     "multiValueQueryStringParameters": None,
#     "pathParameters": {
#         "itemid": "Gautam"
#     },
#     "stageVariables": None,
#     "requestContext": {
#         "resourceId": "gcice4",
#         "resourcePath": "/items/{itemid}",
#         "httpMethod": "PUT",
#         "extendedRequestId": "Fw62ZFVKiYcFxjw=",
#         "requestTime": "04/Jan/2020:07:28:15 +0000",
#         "path": "/items/{itemid}",
#         "accountId": "641484180035",
#         "protocol": "HTTP/1.1",
#         "stage": "test-invoke-stage",
#         "domainPrefix": "testPrefix",
#         "requestTimeEpoch": 1578122895235,
#         "requestId": "eb20f583-eddd-40bb-a1bd-2af8c599e9a9",
#         "identity": {
#             "cognitoIdentityPoolId": None,
#             "cognitoIdentityId": None,
#             "apiKey": "test-invoke-api-key",
#             "principalOrgId": None,
#             "cognitoAuthenticationType": None,
#             "userArn": "arn:aws:iam::641484180035:root",
#             "apiKeyId": "test-invoke-api-key-id",
#             "userAgent": "aws-internal/3 aws-sdk-java/1.11.690 Linux/4.9.184-0.1.ac.235.83.329.metal1.x86_64 OpenJDK_64-Bit_Server_VM/25.232-b09 java/1.8.0_232 vendor/Oracle_Corporation",
#             "accountId": "641484180035",
#             "caller": "641484180035",
#             "sourceIp": "test-invoke-source-ip",
#             "accessKey": "ASIAZKW3PZJBQJYVOQUF",
#             "cognitoAuthenticationProvider": None,
#             "user": "641484180035"
#         },
#         "domainName": "testPrefix.testDomainName",
#         "apiId": "76br69x4ok"
#     },
#     "body": None,
#     "isBase64Encoded": False
# }


def handler(event, context):
    dynamodb_client = boto3.client('dynamodb')
    product = event['pathParameters']['itemid']
    pprint.pprint(event)
    if event['httpMethod'] == 'GET':
        product = event['pathParameters']['itemid']
        response = dynamodb_client.get_item(TableName="inventory", Key={
            'product_id': {'S': product}
        })
        if 'Item' in response:
            item = response["Item"]
        else:
            return result(400, 'item not found')
        # item['Price']['N'] = int(item['Price']['N'])
        return result(200, json.dumps(item))
    # else:
    #     response = dynamodb_client.update_item(TableName='inventory', Key={'product_id': {'S': product}},
    #                                            UpdateExpression='set  = :a')


def result(status, message):
    return {
        'statusCode': status,
        'body': message,
        'headers': {
            'Content-Type': 'application/json'
        }
    }


