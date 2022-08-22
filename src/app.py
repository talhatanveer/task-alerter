import os
from urllib import request
from time import time
from flask import Flask, request, make_response
from utils import (
    send_sms, 
    fetch_csv,
    get_user_index,
    date_modulo
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
    for i in range(0, dbSize):
        phone_number = database[i]['phone number']

        if phone_number != '':
            # rotate chore
            chore = database[date_modulo(dbSize, i)]['chore']
            send_sms(
                f"Your chores for today are: {chore}", 
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