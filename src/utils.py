from twilio.rest import Client
import os, requests

account_sid = os.environ['TWILIO_SID']
auth_token  = os.environ['TWILIO_AUTH_TOKEN']

client = Client(account_sid, auth_token)

def send_sms(number, message):
    message = client.messages.create(
        to=number, 
        from_=os.environ['TWILIO_NUMBER'],
        body=message
    )   

def fetch_csv():
    try:
        response = requests.get(os.environ['CSV_URL'])
        parsed_csv = parse_csv(response.text)
        return list(parsed_csv)
    except Exception as e:
        print(e)
        return False

def parse_csv(str: str):
    lines = str.splitlines()
    data = []
    headers = [x.lower() for x in lines[0].split(',')]
    header_count = len(headers)

    for i in range(1, len(lines)):
        row = lines[i].split(',')
        tmp = {}
        for c in range(0, header_count):
            tmp[headers[c]] = row[c]
        
        data.append(tmp)
    
    return data

def find_user(database, email):
    matches = [x for x in database if x['email'] == email]
    
    if len(matches) == 0:
        return None
    
    return matches[0]

def send_alerts():
    pass