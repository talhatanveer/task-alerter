from twilio.rest import Client
from datetime import datetime, timedelta
from pytz import timezone
import os, requests, csv, time

TZ = timezone('US/Central')

account_sid = os.environ['TWILIO_SID']
auth_token  = os.environ['TWILIO_AUTH_TOKEN']

client = Client(account_sid, auth_token)

start_date = datetime(2022, 8, 20, 10, 0, 0).astimezone(tz = TZ)

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
def date_modulo(n: int, i: int, today = datetime.fromtimestamp(time.time()).astimezone(tz=TZ)):
    delta = (today - start_date).days

    return (i + delta) % n

def get_chore_today(database, i):
    today = datetime.fromtimestamp(time.time()).astimezone(tz = TZ)

    return database[date_modulo(len(database), i, today)]['chore']
    
def days_ahead(database, days, separator="\n"):
    dbSize = len(database)
    today = datetime.fromtimestamp(time.time()).astimezone(tz = TZ)
    # today = datetime(2022, 9, 1, 10, 30, 0).astimezone(tz = TZ)

    days_ahead = {}
    exclude = ["Sat", "Fri"]

    if today.hour < 10:
        i = -1
    else:
        i = 0
    
    count = 0

    while count < days:
        date = (today + timedelta(days = i))
        i += 1

        if date.strftime('%a') in exclude:
            continue
        
        date_str = date.strftime("%a, %b %d")

        for j in range(0, dbSize):
            phone_number = database[j]['phone number']

            # no phone number supplied?
            if phone_number == '':
                continue

            chore = database[date_modulo(dbSize, j + count, today)]

            if phone_number not in days_ahead:
                days_ahead[phone_number] = {
                    "chores": "",
                    "name": database[j]['person'].split(" ")[0]
                }
            
            days_ahead[phone_number]["chores"] += \
                f"{date_str} - {chore['chore']} " + \
                f"(X Penalty: {chore['x penalty']})"

            if count < days - 1:
                days_ahead[phone_number]["chores"] += f"{separator}{separator}"

        count += 1

    return days_ahead

def serve_html(file):
    with open(f"ui/{file}", 'r') as f:
        return f.read()