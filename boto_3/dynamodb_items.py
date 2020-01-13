import boto3
import pprint
import json
from decimal import *
from botocore.exceptions import ClientError
from boto3.dynamodb.conditions import Key, Attr

session = boto3.Session(profile_name="dark_knight")
dynamo = session.resource("dynamodb")

table = dynamo.Table("movies")

# response = table.meta.client.put_item(TableName="User_Table",
#                                       Item={
#                                           'User_ID': "1",
#                                           "First_name": 11232,
#                                           'Last_name': "Kumar"
#                                       },
#                                       ReturnConsumedCapacity='TOTAL'
#                                       )
# pprint.pprint(response['ConsumedCapacity']['CapacityUnits'])

# with open('moviedata.json') as json_file:
#     movies = json.load(json_file, parse_float=Decimal)
#     # title_generator, year_generator, info_generator = (movie.get('title', 'title not found'), int(movie.get('year', 'year not found')), movie.get('info', 'info not found') for movie in movies)
#     for movie in movies:
#         # print(movie.get('info'))
#         year = int(movie.get('year', 'year not found'))
#         title = movie.get('title', 'title not found')
#         info = movie.get('info', 'info not found')
#         data_load = {
#             'year': year,
#             'title': title,
#             'info': info
#         }
#         response = dynamo.meta.client.put_item(TableName="movies",
#                                                Item=data_load, ReturnConsumedCapacity='TOTAL')
#         pprint.pprint(response['ConsumedCapacity']['CapacityUnits'])

#
# class DecimalEncoder(json.JSONEncoder):
#     def default(self, value):
#         if isinstance(value, Decimal):
#             if value % 1 == 0:
#                 return int(value)
#             else:
#                 return float(value)
#         return super(DecimalEncoder, self).default(value)
#
#
year = 2020
title = 'My success story'


# response = dynamo.meta.client.put_item(TableName='movies', Item={
#     'year': year,
#     'title': title,
#     'info': {
#             'plot': "Everything happens all at once",
#             'rating': Decimal(0),
#             'actors': ['No one', 'No one', 'No one']
#     }
# })
# pprint.pprint(response)
# print(json.dumps(response, indent=2, cls=DecimalEncoder))
#
class DecimalEncoder(json.JSONEncoder):
    def default(self, value):
        if isinstance(value, Decimal):
            if value % 1 == 0:
                return int(value)
            else:
                return float(value)
        else:
            return super(DecimalEncoder, self).default(value)


#
#
# title = 'My success story'
# year = 2020
# try:
#     response = dynamo.meta.client.get_item(TableName='movies',
#                                            Key={'year': year, 'title': title})
# except ClientError as e:
#     pprint.pprint(e.response)
# else:
#     item = response['Item']
#     print(json.dumps(item, indent=2, cls=DecimalEncoder))

# response = dynamo.meta.client.update_item(TableName='movies',
#                                           Key={'year': year, 'title': title},
#                                           UpdateExpression='set info.plot = :p, info.rating = :r',
#                                           ExpressionAttributeValues={
#                                               ':r': Decimal('9.8'),
#                                               ':p': "Try to the best of my abilities"
#                                           },
#                                           ReturnValues='UPDATED_NEW'
#                                           )
#
# print(json.dumps(response, indent=2, cls=DecimalEncoder))

# response = dynamo.meta.client.update_item(TableName='movies',
#                                           Key={
#                                               'year': year,
#                                               'title': title
#                                           },
#                                           UpdateExpression='set info.rating = info.rating - :r',
#                                           ExpressionAttributeValues={
#                                               ':r': Decimal(".1")
#                                           },
#                                           ReturnValues='UPDATED_NEW'
#                                           )
# print(json.dumps(response, indent=2, cls=DecimalEncoder))

# response = dynamo.meta.client.update_item(TableName='movies',
#                                           Key={
#                                               'year': year,
#                                               'title': title
#                                           },
#                                           UpdateExpression='set info.actors = :a',
#                                           ConditionExpression='attribute_not_exists(info.actors)',
#                                           ExpressionAttributeValues={
#                                               ':a': "No one"
#                                           },
#                                           ReturnValues='UPDATED_NEW'
#                                           )
#
# print(json.dumps(response, indent=2, cls=DecimalEncoder))


# try:
#     response = dynamo.meta.client.update_item(TableName='movies',
#                                               Key={
#                                                   'year': year,
#                                                   'title': title,
#                                               },
#                                               UpdateExpression='remove info.actors[0]',
#                                               ConditionExpression='size(info.actors) >= :num',
#                                               ExpressionAttributeValues={
#                                                   ':num': 3
#                                               },
#                                               ReturnValues='UPDATED_NEW'
#                                               )
# except ClientError as e:
#     if e.response['Error']['Code'] == 'ConditionalCheckFailedException':
#         print(e.response['Error']['Message'])
#     else:
#         raise
# else:
#     print(json.dumps(response, indent=2, cls=DecimalEncoder))

# try:
#     response = dynamo.meta.client.delete_item(TableName='movies',
#                                               Key={
#                                                   'year': year,
#                                                   'title': title,
#                                               },
#                                               ConditionExpression='size(info.actors) <= :num',
#                                               ExpressionAttributeValues={
#                                                   ':num': 3
#                                               },
#                                               ReturnValues='ALL_OLD'
#                                               )
# except ClientError as e:
#     if e.response['Error']['Code'] == 'ConditionalCheckFailedException':
#         print(e.response['Error']['Message'])
#     else:
#         raise
# else:
#     print(json.dumps(response, indent=2, cls=DecimalEncoder))

# response = dynamo.meta.client.query(TableName='movies', KeyConditionExpression=Key('year').eq(2012))
# for i in response['Items']:
#     print(i['title'], ":", i['year'])

# response = dynamo.meta.client.query(TableName='movies', ProjectionExpression='#yr, title, info.genres, info.actors[0]',
#                                     ExpressionAttributeNames={
#                                         '#yr': 'year'
#                                     },
#                                     KeyConditionExpression=Key('year').eq(2012) & Key('title').between('A', 'M')
#                                     )
# for i in response['Items']:
#     print(json.dumps(i, indent=2, cls=DecimalEncoder))

Proj_Exp = '#yr, title, info.rating'
Express_Attr_Name = {'#yr': 'year'}
Filter_Express = Key("year").between(2000, 2010) & Attr("info.rating").gt(Decimal(7.5))

response = dynamo.meta.client.scan(TableName='movies', FilterExpression=Filter_Express, ProjectionExpression=Proj_Exp,
                                   ExpressionAttributeNames=Express_Attr_Name)
# for i in response['Items']:
#     print(json.dumps(i, cls=DecimalEncoder, indent=2))
print(response)

while 'LastEvaluatedKey' in response:
    response = dynamo.meta.client.scan(TableName='movies', FilterExpression=Filter_Express,
                                       ProjectionExpression=Proj_Exp,
                                       ExpressionAttributeNames=Express_Attr_Name, ExclusiveStartKey=response["LastEvaluatedKey"])
    print(response)
