import schoolsoft_api
import json
import googleapiclient.discovery
import typing
from period import Period
from datetime import datetime
from google.oauth2.credentials import Credentials
import google_auth_oauthlib.flow
from flask import Flask, redirect, session, url_for, request, make_response
import flask_session
import typing

def getPeriods(api: schoolsoft_api.Api):
    lessons = api.lessons
    for lesson in lessons:
        weekraw = lesson["weeksString"].split(", ")
        weekset = set()
        for weekrange in weekraw:
            _weekspl = weekrange.split("-")
            print(_weekspl)
            if _weekspl[0]: weekset.update(range(int(_weekspl[0]), int(_weekspl[-1])+1))
        print(lesson["subjectName"])
        if weekset: yield Period(
            api,
            name = lesson["subjectName"], 
            weeks = weekset, 
            weekday = lesson["dayId"], 
            time = datetime.strptime(lesson["startTime"], "%Y-%m-%d %H:%M:%S.%f"), 
            end = datetime.strptime(lesson["endTime"], "%Y-%m-%d %H:%M:%S.%f"), 
            conversion = {"En": "English"}
        )


def addPeriodsToCalendar(periods: typing.Iterable[Period], credentials: dict):
    with googleapiclient.discovery.build("calendar", "v3", credentials=Credentials(**credentials)) as service:
        calendar = service.calendars().get(calendarId='primary').execute()
        print(calendar['summary'])






def generateAuthURL() -> tuple[str, str]:
  flow = google_auth_oauthlib.flow.Flow.from_client_secrets_file(
    'client_secret.json',
    scopes=scopes
  )
  flow.redirect_uri = url + url_for("callback")
  print(url + url_for("callback"))
  return flow.authorization_url(
      access_type='offline',
      include_granted_scopes='true'
  )

scopes = ["https://www.googleapis.com/auth/calendar"]
flask = Flask(__name__)

@flask.route("/")
def index():
  username = ""
  try:
    if "credentials" in session:
      with googleapiclient.discovery.build("oauth2", "v2", credentials=Credentials(**session["credentials"])) as uiendp:
        username = uiendp.userinfo().get().execute()["name"]
  except Exception as e:
     print(e)
  finally:
    return f"""
    <!DOCTYPE html>
    <html>
      <head>
        <meta charset="UTF-8">
        <title>Schoolsoft-Cal Linker</title>
      </head>
      <body>
        <h2>Copy classes to Calendar</h2>
        {f'''
        <a href="{generateAuthURL()[0]}">Log in with Google</a>
        ''' if ("credentials" not in session) or not username else f'''
        <form method="post" action="/login">
          <p>Logged in as <b>{username}</b></p>
          <p>SchoolSoft User: <input type=text name="ssUsr" required/></p>
          <p>SchoolSoft Password: <input type=passwd name="ssPwd" required/></p>
          <p>School ID: <input type=text name="ssSchool" required/></p>
          <p>Name of calendar: <input type=text name="gCal" required/></p>
          <input type=submit value="Copy to Calendar"/>
        </form>
       '''}
      </body>
    </html>
  """



states = {}
@flask.route("/callback", methods=["GET","POST"])
def callback():
  state = request.args['state']
  flow = google_auth_oauthlib.flow.Flow.from_client_secrets_file(
    'client_secret.json',
    scopes=scopes,
    state=state)
  flow.redirect_uri = url + url_for("callback")

  authorization_response = request.url
  print(authorization_response)
  flow.fetch_token(authorization_response=authorization_response)
    
  credentials = flow.credentials
  session['credentials'] = {
    'token': credentials.token,
    'refresh_token': credentials.refresh_token,
    'token_uri': credentials.token_uri,
    'client_id': credentials.client_id,
    'client_secret': credentials.client_secret,
    'scopes': credentials.scopes}
  
  return redirect(url + url_for("index"))

  
import os 
os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'

url = "https://bbb5-84-218-4-74.eu.ngrok.io"

SESSION_TYPE = "redis"
PERMANENT_SESSION_LIFETIME = 1800

flask.secret_key = os.urandom(24)
flask.config['SESSION_TYPE'] = 'filesystem'
flask_session.Session(flask)
flask.run("localhost", 80, True)
    

  
