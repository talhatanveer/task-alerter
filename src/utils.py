from twilio.rest import Client
import os, requests

account_sid = os.environ['TWILIO_SID']
auth_token  = os.environ['TWILIO_AUTH_TOKEN']

client = Client(account_sid, auth_token)

def send_sms(number, message):
    message = client.messages.create(
        to=number, 
        from_=os.environ['TWILIO_NUMBER'],
        body=message)


def fetch_csv():
    return requests.get(os.environ['CSV_URL'])

def send_alerts():
    pass