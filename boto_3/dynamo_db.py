import boto3
import pprint

session = boto3.Session(profile_name="dark_knight")
dynamo_db = session.resource("dynamodb")
# table = dynamo_db.create_table(
#     AttributeDefinitions=[
#         {
#             'AttributeName': 'First_Name',
#             'AttributeType': 'S'
#         },
#         {
#             'AttributeName': 'Last_Name',
#             'AttributeType': 'S'
#         }
#     ],
#     TableName='Sample_table',
#     KeySchema=[
#         {
#             'AttributeName': 'First_Name',
#             'KeyType': 'HASH'
#         },
#         {
#             'AttributeName': 'Last_Name',
#             'KeyType': 'RANGE'
#         }
#     ],
#     ProvisionedThroughput={
#         'ReadCapacityUnits': 1,
#         'WriteCapacityUnits': 1
#     },
#     Tags=[
#         {
#             'Key': 'Name',
#             'Value': 'Sample_Table'
#         },
#     ]
#     )
# table.meta.client.get_waiter('table_exists').wait(TableName='Sample_table')
# print(table.item_count)

# list_of_all_tables = dynamo_db.meta.client.list_tables()
# print(list_of_all_tables['TableNames'])
#
# response = dynamo_db.meta.client.describe_table(TableName="Job_Table")
# pprint.pprint(response)

updating = dynamo_db.meta.client.update_table(TableName="User_Table",
                                              ProvisionedThroughput=
                                              {
                                                  'ReadCapacityUnits': 1,
                                                  'WriteCapacityUnits': 1
                                              }
                                              )
table = dynamo_db.Table("User_Table")
table.meta.client.get_waiter('table_exists').wait(TableName='User_Table')
response_1 = dynamo_db.meta.client.describe_table(TableName="User_Table")
pprint.pprint(response_1)
