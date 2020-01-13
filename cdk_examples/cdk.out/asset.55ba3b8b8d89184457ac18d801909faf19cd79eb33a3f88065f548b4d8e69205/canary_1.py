import requests
import os
import datetime

SITE = os.environ['site']
EXPECTED = os.environ['expected']


def validate(res):
    return EXPECTED in res


def lambda_handler(event, context):
    print(f"Test the site{SITE} at the time {event['time']}")
    response = requests.get(url="https://www.amazon.in", headers={'User-Agent': 'AWS Lambda'})
    try:
        if not validate(response.text):
            raise Exception("Validation failed")
    except:
        print("Check failed")
    else:
        print("okay")
    finally:
        print(f"Check complete at {str(datetime.datetime.now())}")
