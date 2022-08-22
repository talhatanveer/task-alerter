from twilio.rest import Client
from datetime import datetime
from pytz import timezone
import os, requests, csv, time

TZ = timezone('US/Central')

account_sid = os.environ['TWILIO_SID']
auth_token  = os.environ['TWILIO_AUTH_TOKEN']

client = Client(account_sid, auth_token)

start_date = datetime(2022, 8, 21, 16, 0, 0).astimezone(tz = TZ)

def send_sms(message: str, number: str):
    message = client.messages.create(
        to=number, 
        from_=os.environ['TWILIO_PHONE_NUMBER'],
        body=message
    )

def fetch_csv():
    try:
        response = requests.get(os.environ['CSV_URL'])
        rows = list(csv.reader(response.text.splitlines()))
        return parse_csv(rows)
    except Exception as e:
        print(e)
        return False

def parse_csv(lines: list):
    data = []
    headers = [x.lower() for x in lines[0]]
    header_count = len(headers)

    for i in range(1, len(lines)):
        row = lines[i]
        tmp = {}
        for c in range(0, header_count):
            tmp[headers[c]] = row[c]
        
        data.append(tmp)
    
    return data

def find_user(database: list, email: str):
    matches = [x for x in database if x['email'] == email]
    
    if len(matches) == 0:
        return None
    
    return matches[0]


def get_user_index(database: str, email: list):
    for i in range(0, len(database)):
        if database[i]['email'].lower() == email.lower():
            return i

    return None

# automatically rotate chores
# chores rotate 10:00 a.m. at the specified timezone
def date_modulo(n: int, i: int, offset = 0):
    today = datetime.fromtimestamp(time.time()).astimezone(tz=TZ)
    delta = (today - start_date).days

    # if time falls between 00:00 and 10:00, subtract a day
    if today.hour > 0 and today.hour < 10 and delta != 0:
        delta -= 1

    return (i + delta + offset) % n