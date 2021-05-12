from decouple import config
from google.oauth2 import service_account
import googleapiclient.discovery

CAL_ID = config('CAL_ID')
SCOPES = ['https://www.googleapis.com/auth/calendar']
SERVICE_ACCOUNT_FILE = './google-credentials.json'

def populate_google_calendar(all_weeks):
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
        print("DELETED", event_id)

    # FILL GOOGLE CAL WITH ALL WEEK EVENTS IN DB


    for week in all_weeks:
        print(week)
        new_event = {
        'summary': f"{week.owner_group}'s Week",
        'location': 'Fire Land D, Lovell, ME',
        'description': 'A sample description',
        'start': {
            'date': f"{week.start_date}",
            'timeZone': 'America/New_York',
        },
        'end': {
            'date': f"{week.start_date}",
            'timeZone': 'America/New_York',
        },
        }
        print(new_event)
        service.events().insert(calendarId=CAL_ID, body=new_event).execute()
        print('Event created: %s' % (new_event.get('htmlLink')))


