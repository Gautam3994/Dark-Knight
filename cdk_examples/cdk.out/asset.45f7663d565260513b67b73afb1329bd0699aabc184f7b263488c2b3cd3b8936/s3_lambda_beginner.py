import json


def main(event, context):
    event_string = json.dumps(event, indent=2)
    print(event_string)
    context_string = json.dumps(context, indent=2)
    print(context_string)
    for record in event['records']:
        print(record)
        file = {
            'bucket': record['s3']['bucket']['name'],
            'key': record['s3']['object']['key']
        }
        print(json.dumps(file))
