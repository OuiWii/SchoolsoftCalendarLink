import schoolsoft_api
import json
import googleapiclient.discovery
import typing
from period import Period
from datetime import datetime

api = schoolsoft_api.Api("wier", "Henrik11", "fredsborgskolan")

def getPeriods():
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


def addPeriodsToCalendar(periods: typing.Iterable[Period]):
    with googleapiclient.discovery.build("calendar", "v3") as service:
        calendar = service.calendars().get(calendarId='primary').execute()
        print(calendar['summary'])

for p in getPeriods(): print(p)

import google.oauth2.credentials
import google_auth_oauthlib.flow
from flask import Flask, redirect, session, url_for, request
import typing, asyncio





def generateAuthURL() -> tuple[str, str]:
  return flow.authorization_url(
      include_granted_scopes='true'
  )

scopes = ["https://googleapis.com/auth/calendar"]
flow = google_auth_oauthlib.flow.Flow.from_client_secrets_file(
    'client_secret.json',
    scopes=scopes
)
flask = Flask("GoogleAuth")

@flask.route("/")
def index():
  with open("html/index.html") as f: return f.read()

@flask.route("/callback", methods=["GET", "POST"])
def authendpoint():
  state = session['state']
  flow = google_auth_oauthlib.flow.Flow.from_client_secrets_file(
    'client_secret.json',
    scopes=self._scopes,
    state=state)
  flow.redirect_uri = url_for('oauth2callback', _external=True)

  authorization_response = request.url
  flow.fetch_token(authorization_response=authorization_response)
    
  credentials = flow.credentials
  session['credentials'] = {
    'token': credentials.token,
    'refresh_token': credentials.refresh_token,
    'token_uri': credentials.token_uri,
    'client_id': credentials.client_id,
    'client_secret': credentials.client_secret,
    'scopes': credentials.scopes}

  



flask.run()
    

  