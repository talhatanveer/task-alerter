# Task Alerter
A hobby project to manage chores for my fraternity. Sends alerts via text message and includes some basic endpoints for pulling informaton from a remote csv file (e.g. you can build a shortcut to get a chore with ioS Shortcuts). Uses a remotely hosted CSV file as its database (e.g. Google Sheets).


## Environment Variables
| Env Var             | Description                     |
|---------------------|---------------------------------|
| TWILIO_SID          | Your Twilio SID                 |
| TWILIO_AUTH_TOKEN   | Your Twilio Authorization Token |
| TWILIO_PHONE_NUMBER | Your Twilio Phone Number        |
| CSV_URL             | URL To Your CSV File            |
| API_KEY             | API Key Value for Authorization |
| PORT                | Port Number To Run Server On    |
| ADMIN_KEY           | Authorization for Admin Endpoints |

`A template CSV file has been included`


## Issues
- Need to generate `requirements.txt` manually because `-r` is not an option when pipenv is run in Docker
