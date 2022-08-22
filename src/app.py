import os
from urllib import request
from time import time
from datetime import datetime, timedelta
from flask import Flask, request, make_response
from utils import (
    send_sms, 
    fetch_csv,
    get_user_index,
    date_modulo,
    TZ
)

API_KEY = os.environ['API_KEY']
ADMIN_KEY = os.environ['ADMIN_KEY']
PORT = os.environ['PORT']

SEND_WAIT = 120 # in seconds
LAST_SEND = 0 # unix timestamp in seconds

app = Flask(__name__)

# AUTHENTICATION
@app.before_request
def auth():
    try:
        key = request.headers['api-key']
    except Exception as e:
        key = False
    finally:
        if key != API_KEY:
            response = make_response({'message':'An invalid or no API Key was supplied'})
            response.status_code = 403
            return response

# SEND OUT CHORES
@app.route("/chores", methods=["POST"])
def send_chores():
    global SEND_WAIT, LAST_SEND

    if time() - LAST_SEND < SEND_WAIT:
        return {'message':'You tried to send out chores again too early'}
    
    LAST_SEND = time()

    database = fetch_csv()
    dbSize = len(database)
    today = datetime.fromtimestamp(time()).astimezone(tz = TZ)

    week_ahead = {}
    exclude = ["Sat", "Fri"]
    i = 0
    count = 0

    while count < 7:
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

            chore = database[date_modulo(dbSize, i, count)]

            if phone_number not in week_ahead:
                week_ahead[phone_number] = {
                    "chores": "",
                    "name": database[j]['person'].split(" ")[0]
                }
            
            week_ahead[phone_number]["chores"] += \
                f"{date_str} - {chore['chore']} " + \
                f"(X Penalty: {chore['x penalty']})"

            if count < 6:
                week_ahead[phone_number]["chores"] += "\n\n"

        count += 1

    # print(week_ahead)

    for phone_number in week_ahead:
        message = \
            f"Hey {week_ahead[phone_number]['name']}, " + \
            f"your chores for the next 7 days are:" + \
            f"\n\n{week_ahead[phone_number]['chores']}"
        
        send_sms(
            message, 
            f"+{phone_number}"
        )
    
    return {'message':'Chores have been sent out!'}

# GET A SINGLE CHORE
@app.route("/chores", methods=["GET"])
def get_chore():
    email = request.args.get('email')

    if email == None or email == '':
        return {'chore':'No email was supplied', 'message': 'No chore was supplied'}

    database = fetch_csv()
    user_idx = get_user_index(database, email)

    if user_idx == None:
        return {
            'chore': 'Could not find a chore for the given email',
            'message': 'Could not find a chore for the given email'
        }

    user = database[date_modulo(len(database), user_idx)]

    return {'chore': user['chore'], 'message': user['chore']}

# support for old route after refactor
@app.route("/chore", methods=["GET"])
def _get_chore():
    return get_chore()

# FLASK SERVER
if __name__ == "__main__":
    from waitress import serve
    print(f"Server started on 0.0.0.0:{PORT}")
    serve(app, host="0.0.0.0", port=PORT)