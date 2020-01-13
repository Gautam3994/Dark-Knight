import random
# import string
#
#
# model_number = []
# value = "".join(random.choices((string.ascii_letters+string.digits), k=8))
# print(value)
from faker import Faker
fake = Faker()

any = {
    "resource": "/order",
    "path": "/order",
    "httpMethod": "POST",
    "headers": None,
    "multiValueHeaders": None,
    "queryStringParameters": None,
    "multiValueQueryStringParameters": None,
    "pathParameters": None,
    "stageVariables": None,
    "requestContext": {
        "resourceId": "ohs7tm",
        "resourcePath": "/order",
        "httpMethod": "POST",
        "extendedRequestId": "GExBqGpDiYcFhWQ=",
        "requestTime": "10/Jan/2020:07:59:19 +0000",
        "path": "/order",
        "accountId": "641484180035",
        "protocol": "HTTP/1.1",
        "stage": "test-invoke-stage",
        "domainPrefix": "testPrefix",
        "requestTimeEpoch": 1578643159311,
        "requestId": "14001b0d-d198-4a89-af61-0bdede5c4215",
        "identity": {
            "cognitoIdentityPoolId": None,
            "cognitoIdentityId": None,
            "apiKey": "test-invoke-api-key",
            "principalOrgId": None,
            "cognitoAuthenticationType": None,
            "userArn": "arn:aws:iam::641484180035:root",
            "apiKeyId": "test-invoke-api-key-id",
            "userAgent": "aws-internal/3 aws-sdk-java/1.11.690 Linux/4.9.184-0.1.ac.235.83.329.metal1.x86_64 OpenJDK_64-Bit_Server_VM/25.232-b09 java/1.8.0_232 vendor/Oracle_Corporation",
            "accountId": "641484180035",
            "caller": "641484180035",
            "sourceIp": "test-invoke-source-ip",
            "accessKey": "ASIAZKW3PZJB4ILIU7XG",
            "cognitoAuthenticationProvider": None,
            "user": "641484180035"
        },
        "domainName": "testPrefix.testDomainName",
        "apiId": "j9wdhnxdi1"
    },
    "body": "{\n    \"order_id\": \"ws23234\"\n}",
    "isBase64Encoded": False
}


print(any['body'])
