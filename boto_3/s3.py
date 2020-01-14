import uuid
import boto3
import pprint
session = boto3.Session(profile_name="dark_knight")
current_region = session.region_name
s3_resource = session.resource('s3')


def create_bucket_aws(bucket_prefix, s3_connection):
    bucket_name = ''.join([bucket_prefix, str(uuid.uuid4())])
    bucket_response = s3_connection.create_bucket(Bucket=bucket_name, CreateBucketConfiguration={
        "LocationConstraint": current_region
    })
    return bucket_name, bucket_response


def create_file_in_bucket(file_suffix, file_content, file_size):
    file_name_aws = ''.join([str(uuid.uuid4().hex[:6]), file_suffix])
    with open(file_name_aws, 'w') as file:
        file.write(str(file_content) * file_size)
    return file_name_aws


def copy_paste_bucket(copy_from_bucket, copy_to_bucket, filename):
    copy_source = {
        "Bucket": copy_from_bucket,
        "Key": filename
    }
    s3_resource.Object(bucket_name=copy_to_bucket, key=filename).copy(copy_source)


first_bucket_name, first_bucket_creation = create_bucket_aws('gautam', s3_connection=s3_resource.meta.client)
# second_bucket_name, second_bucket_creation = create_bucket_aws('dark', s3_connection=s3_resource.meta.client)
first_file_name = create_file_in_bucket("dark", "Gautam", 300)
# second_file_name = create_file_in_bucket("darkknight", "Kumar", 300)
# this_bucket = s3_resource.Bucket(name=first_bucket_name).upload_file() Alter to below : Creating bucket object to upload file
upload_object = s3_resource.Object(bucket_name=first_bucket_name, key=first_file_name).upload_file(Filename=first_file_name, ExtraArgs={
    "ACL": "public-read",
    "ServerSideEncryption": "AES256"
})
# upload_object_1 = s3_resource.Object(bucket_name=first_bucket_name, key=second_file_name).upload_file(Filename=second_file_name)
download_object = s3_resource.Object(bucket_name=first_bucket_name, key=first_file_name).download_file(f'D:/All Downloads/{first_file_name}')
# copy_paste_bucket(first_bucket_name,  second_bucket_name, first_file_name)
# s3_resource.Bucket("dark17e500f9-4815-4125-b64d-c08eab36cb23").delete()
for a_bucket in s3_resource.buckets.all():
    print(a_bucket)

# object_acl = s3_resource.ObjectAcl('darkd9fc45df-8bba-4246-860f-fc145525e2c7', 'f4b0d2dark')
# object_acl.put(ACL='private')
# print(object_acl.grants)

print(upload_object.server_side_encryption)
