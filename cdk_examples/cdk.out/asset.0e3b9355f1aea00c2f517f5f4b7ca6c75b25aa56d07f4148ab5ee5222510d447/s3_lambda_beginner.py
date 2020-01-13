import json


def main(event, context):
    event_string = json.dumps(event, indent=2)
    print(event_string)
    print(context)
    for record in event['Records']:
        print(record)
        file = {
            'bucket': record['s3']['bucket']['name'],
            'key': record['s3']['object']['key']
        }
        print(json.dumps(file))
