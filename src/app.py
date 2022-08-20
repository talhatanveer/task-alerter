import json, os
from urllib import request
from flask import Flask, request, make_response
from utils import send_sms, fetch_csv, find_user

API_KEY = os.environ['API_KEY']
PORT = os.environ['PORT']

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
            response = make_response('{}')
            response.status_code = 403
            return response

# SEND OUT CHORES
@app.route("/chores", methods=["POST"])
def send_chores():
    
    database = fetch_csv()
    for user in database:
        phone_number = user['phone number']

        if phone_number != '':
            send_sms(
                f"Hey {user['person']}, your chores for today are: {user['chore']}", 
                f"+{phone_number}"
            )
    
    return {}

# GET A SINGLE CHORE
@app.route("/chore", methods=["GET"])
def get_chore():
    email = request.args.get('email')

    if email == None or email == '':
        return {'chore':'No email was supplied'}

    database = fetch_csv()
    user = find_user(database, email.lower())

    if user == None:
        return {'chore': 'Could not find a chore for the given email'}

    return {'chore': user['chore']}


# FLASK SERVER
if __name__ == "__main__":
    from waitress import serve
    print(f"Server started on 0.0.0.0:{PORT}")
    serve(app, host="0.0.0.0", port=PORT)