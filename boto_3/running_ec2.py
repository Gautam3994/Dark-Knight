import boto3
import pprint

root_session = boto3.Session(profile_name="dark_knight", region_name="us-east-2")
ec2_resource = root_session.resource('ec2')
ec2_client = root_session.client('ec2')

# for single in ec2_resource.instances.all():
#     print(single.id, single.state['Name'])

for details in ec2_client.describe_instances()['Reservations']:
    pprint.pprint(details)
