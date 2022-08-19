import time, os
from urllib import request
from twilio.rest import Client
from flask import Flask, request, make_response
from utils import send_sms, fetch_csv

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
@app.route("/deploy", methods=["GET"])
def hello_world():
    return "<p>Hello, World!</p>"

# GET A SINGLE CHORE
@app.route("/chore", methods=["GET"])
def get_chore():
    args = request.args
    print(args)


# FLASK SERVER
if __name__ == "__main__":
    from waitress import serve
    print(f"Server started on 0.0.0.0:{PORT}")
    serve(app, host="0.0.0.0", port=PORT)