from jinja2 import Template
import boto3
import datetime

from_address = "gautam3994@gmail.com"
employee = [{
    'Name': "Gautam Kumar",
    "Email": "mgautam3994@gmail.com"
}]
clients = [
    {
        "Name": "Dark Knight",
        "Email": "darknightv907@gmail.com",
        "petname": "Simba"
    },
    {
        "Name": "Devi Kumaresan",
        "Email": "gautam3994@gmail.com",
        "petname": "Tiger"
    }
]
# key_1 = 'templates/come_to_work.html'
# name = employee[0]['Name']
templates_bucket_name = "htmltemplatesbucketv907"


def get_first_name(name):
    first_name, last_name = name.split()
    return first_name


def html_template(key):
    s3 = boto3.resource('s3')
    object_ = s3.Object(templates_bucket_name, key)
    try:
        template = Template(object_.get()['Body'].read().decode('utf-8'))
    except:
        print("unable to load template")
        raise
    else:
        return template


def render_come_to_work_template(name):
    subject = "come to work reminder"
    come_to_work_template = html_template("templates/come_to_work.html")
    html_mail = come_to_work_template.render(first_name=get_first_name(name))
    plain_text_mail = f"Hi {get_first_name(name)}, Please come to work at 8 A.M"
    return subject, html_mail, plain_text_mail


def render_daily_task_template():
    subject = "Daily tasks"
    daily_tasks_template = html_template("templates/daily_tasks.html")
    tasks = {
        'Monday': '1. Clean the dog areas\n',
        'Tuesday': '1. Clean the cat areas\n',
        'Wednesday': '1. Feed the aligator\n',
        'Thursday': '1. Clean the dog areas\n',
        'Friday': '1. Clean the cat areas\n',
        'Saturday': '1. Relax!\n2. Play with the puppies! It\'s the weekend!',
        'Sunday': '1. Relax!\n2. Play with the puppies! It\'s the weekend!'
    }
    days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
    today = days[datetime.date.today().weekday()]
    html_mail = daily_tasks_template.render(day_of_week=today, daily_tasks=tasks[today])
    plaintext_email = (
        "Remember to do all of these today:\n"
        "1. Feed the dogs\n"
        "2. Feed the rabbits\n"
        "3. Feed the cats\n"
        "4. Feed the turtles\n"
        "5. Walk the dogs\n"
        "6. Empty cat litterboxes\n"
        "And:\n"
        "{0}".format(tasks[today])
    )
    return subject, html_mail, plaintext_email


def render_pickup_template(name, pet_name):
    subject = "Pick up your pet"
    pick_up_template = html_template("templates/pickup.html")
    html_mail = pick_up_template.render(first_name=get_first_name(name), pet_name=pet_name)
    plaintext_email = f'Hi {get_first_name(name)}, Please pick up {pet_name} from the pet store'
    return subject, html_mail, plaintext_email


def send_mail_using_templates(subject, html_mail, plaintext_email, receiptients):
    try:
        ses_client = boto3.client('ses', region_name='ap-south-1')
        response = ses_client.send_email(
            Source=from_address,
            Destination={
                'ToAddresses': [receiptients]
            },
            Message={
                "Subject": {
                    'Data': subject
                },
                'Body': {
                    'Text':
                        {
                            'Data': plaintext_email
                        },
                    'Html':
                        {
                            'Data': html_mail
                        }
                }
            },
            ReplyToAddresses=[from_address]
        )

    except Exception as e:
        print(e)
        raise e


def handler(event, context):
    trigger = event['resources'][0]
    print(f'triggered by {trigger}')
    if 'pickup_schedule' in trigger:
        for i in range(len(clients)):
            subject, html_mail, plaintext_email = render_pickup_template(clients[i].get('Name'),
                                                                         clients[i].get('petname'))
            send_mail_using_templates(subject, html_mail, plaintext_email, clients[i].get('Email'))
    elif 'daily_tasks_schedule' in trigger:
        subject_, html_mail_, plaintext_email_ = render_daily_task_template()
        send_mail_using_templates(subject_, html_mail_, plaintext_email_, employee[0]['Email'])
    elif 'wake_up_message_schedule' in trigger:
        subject_1, html_mail_1, plaintext_email_1 = render_come_to_work_template(employee[0]['Name'])
        send_mail_using_templates(subject_1, html_mail_1, plaintext_email_1, employee[0]['Email'])
    else:
        return 'No template for this event'



