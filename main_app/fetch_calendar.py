from __future__ import print_function
import datetime
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials

from decouple import config

# If modifying these scopes, delete the file token.json.
SCOPES = ['https://www.googleapis.com/auth/calendar.readonly']


def get_upcoming_events(number_of_events, display_year):
    """Shows basic usage of the Google Calendar API.
    Prints the start and name of the next 10 events on the user's calendar.
    """
    creds = None
    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'main_app/credentials.json', SCOPES)
            creds = flow.run_local_server(port=8080)
        # Save the credentials for the next run
        with open('token.json', 'w') as token:
            token.write(creds.to_json())

    service = build('calendar', 'v3', credentials=creds)

    # Call the Calendar API
    display_start = datetime.datetime.utcnow().isoformat() + 'Z' # 'Z' indicates UTC time
    print(display_start)
    print(f'Getting the upcoming {number_of_events} events')
    events_result = service.events().list(calendarId='92vin6vuv0aqqvqtnmcjq1lq1s@group.calendar.google.com', timeMin=display_start, 
                                        maxResults=number_of_events, singleEvents=True,
                                        orderBy='startTime').execute()
    events = events_result.get('items', [])

    cleaned_events = []
    
    if not events:
       return cleaned_events
 
    for event in events:
        start_date = event["start"]["date"]
        detail = event['summary']
        print(start_date, detail)
        clean_event = {"start_month_date": start_date[5:], "detail": detail, "year":start_date[0:4]}
        # print(">",int(clean_event["year"]), ">>", type(display_year))
        if int(clean_event["year"]) == display_year:
            cleaned_events.append(clean_event)
        print(cleaned_events)
        # start = event['start'].get('dateTime', event['start'].get('date'))
        # print(start, event['summary'])

    return cleaned_events

# if __name__ == '__get_next_10_events__':
#     main()