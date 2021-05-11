from decouple import config
from google.oauth2 import service_account
import googleapiclient.discovery

CAL_ID = config('CAL_ID')
SCOPES = ['https://www.googleapis.com/auth/calendar']
SERVICE_ACCOUNT_FILE = './google-credentials.json'




#   'recurrence': [
#     'RRULE:FREQ=DAILY;COUNT=2'
#   ],
#   'attendees': [
#     {'email': 'lpage@example.com'},
#     {'email': 'sbrin@example.com'},
#   ],
#     'reminders': {
#     'useDefault': False,
#     'overrides': [
#       {'method': 'email', 'minutes': 24 * 60},
#       {'method': 'popup', 'minutes': 10},
#     ],
#   },



def populate_google_calendar():
    credentials = service_account.Credentials.from_service_account_file(SERVICE_ACCOUNT_FILE, scopes=SCOPES)
    service = googleapiclient.discovery.build('calendar', 'v3', credentials=credentials)

    events_result = service.events().list(calendarId=CAL_ID).execute()
    events = events_result.get('items', [])
    event_id = events[0]['id']
    #  event = events[0]
    # service.events().update(calendarId=CAL_ID, eventId=event_id, body={"end":{"date":"2021-05-25"},"start":{"date":"2021-05-25"},"summary":"Little Cabin"}).execute()

    # DELETE ALL EXISTING EVENTS
    for e in events:
        event_id = e['id']
        service.events().delete(calendarId=CAL_ID, eventId=event_id).execute()

    # FILL GOOGLE CAL WITH ALL WEEK EVENTS IN DB
    # ! need to do this
    new_event = {
    'summary': 'Tom Week',
    'location': 'Fire Land D, Lovell, ME',
    'description': 'A sample description',
    'start': {
        'date': '2021-05-28',
        'timeZone': 'America/New_York',
    },
    'end': {
        'date': '2021-05-28',
        'timeZone': 'America/New_York',
    },
    }
    new_event = service.events().insert(calendarId=CAL_ID, body=new_event).execute()
    print('Event created: %s' % (new_event.get('htmlLink')))
