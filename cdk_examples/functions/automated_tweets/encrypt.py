import base64
import boto3
import json

# session = boto3.Session(profile_name='test_user')
kms = boto3.client('kms')


def encrypt(app_key, kms_key):
    encrypted_app_key = kms.encrypt(KeyId=kms_key, Plaintext=app_key)
    cypert_text = base64.b64encode(encrypted_app_key['CiphertextBlob'])
    return cypert_text


def create_encryptedfile(key_description, source_file, dest_file):
    response = kms.list_keys()
    empty = {}
    for a_key in response["Keys"]:
        des = kms.describe_key(KeyId=a_key['KeyArn'])
        # '''description - changes this for further use'''
        if des['KeyMetadata']['Description'] == key_description and des['KeyMetadata']['KeyState'] == 'Enabled':
            kms_key = des['KeyMetadata']['KeyId']
            # change unencrypted file
            with open(source_file) as creds:
                json_2 = json.loads(creds.read())
                for app_key in json_2.items():
                    encrypted_data = encrypt(app_key[1], kms_key)
                    empty[app_key[0]] = encrypted_data.decode("utf-8")
                    # change encrypted dest file name
                    with open(dest_file, 'w') as encrypt_file:
                        json.dump(empty, encrypt_file, indent=2)


create_encryptedfile("keys for twitter api", 'creds.json', 'encrypted_creds.json')

