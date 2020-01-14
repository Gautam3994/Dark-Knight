import random
import json
import boto3
import base64
from twython import Twython

# session = boto3.Session(profile_name='test_user')
kms = boto3.client('kms')


def decrypt_1(app_key):
    response = kms.decrypt(CiphertextBlob=app_key)
    return response['Plaintext']


with open('encrypted_creds.json') as creds:
    keys_1 = json.loads(creds.read())

consumer_key = decrypt_1(base64.b64decode(keys_1["API_key"].encode('utf-8')))
consumer_secret = decrypt_1(base64.b64decode(keys_1["API_secret_key"].encode('utf-8')))
access_token_key = decrypt_1(base64.b64decode(keys_1["Access_token"].encode('utf-8')))
access_token_secret = decrypt_1(base64.b64decode(keys_1["Access_token_secret"].encode('utf-8')))

twitter = Twython(consumer_key, consumer_secret,
                  access_token_key, access_token_secret)

# Sample random tweets
potential_tweets = [
    'This is my first ever tweet and it is automated',
    'The code for this is written in Python',
    'I am a future Machine Learning Engineer'
]


def send_tweet(tweet_text):
    """Sends a tweet to Twitter"""
    twitter.update_status(status=tweet_text)


def handler(event, context):
    """Sends random tweet from list of potential tweets"""
    send_tweet(random.choice(potential_tweets))


