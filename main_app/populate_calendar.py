from decouple import config
from google.oauth2 import service_account
import googleapiclient.discovery
import datetime

CAL_ID = config('CAL_ID')
SCOPES = ['https://www.googleapis.com/auth/calendar']
SERVICE_ACCOUNT_FILE = './google-credentials.json'



def swap_weeks_google_calendar(desired_week, offered_week):
    credentials = service_account.Credentials.from_service_account_file(SERVICE_ACCOUNT_FILE, scopes=SCOPES)
    service = googleapiclient.discovery.build('calendar', 'v3', credentials=credentials)

    events_result = service.events().list(calendarId=CAL_ID, maxResults=2500).execute()
    events = events_result.get('items', [])

    # FIND THE 2 MATCHING EVENTS
    desired_event_id = ""
    offered_event_id = ""

    for event in events:
        if event["start"]["date"] == str(desired_week.start_date):
            desired_event_id = event["id"]
        if event["start"]["date"] == str(offered_week.start_date):
            offered_event_id = event["id"]

    # SWAP AND THEN UPDATE GCAL
    if desired_event_id and offered_event_id:

        service.events().patch(calendarId=CAL_ID, eventId=desired_event_id, body={"end":{"date":f'{offered_week.start_date + datetime.timedelta(days=7)}'},"start":{"date":f'{offered_week.start_date}'},'summary': f"{offered_week.owner_group}'s Week",}).execute()
        service.events().patch(calendarId=CAL_ID, eventId=offered_event_id, body={"end":{"date":f'{desired_week.start_date + datetime.timedelta(days=7)}'},"start":{"date":f'{desired_week.start_date}'},'summary': f"{desired_week.owner_group}'s Week",}).execute()
    else:
        print("Problem swapping gcal weeks")


def populate_google_calendar(all_weeks):
    
    credentials = service_account.Credentials.from_service_account_file(SERVICE_ACCOUNT_FILE, scopes=SCOPES)
    service = googleapiclient.discovery.build('calendar', 'v3', credentials=credentials)

    events_result = service.events().list(calendarId=CAL_ID, maxResults=2500).execute()
    events = events_result.get('items', [])
    
    # DELETE ALL EXISTING EVENTS
    for e in events:
        event_id = e['id']
        service.events().delete(calendarId=CAL_ID, eventId=event_id).execute()
        print("DELETED ", event_id)

    # FILL GOOGLE CAL WITH ALL WEEK EVENTS IN DB


    for week in all_weeks:
        new_event = {
        'summary': f"{week.owner_group}'s Week",
        'location': 'Fire Land D, Lovell, ME',
        'description': 'https://littlecabin.herokuapp.com',
        'start': {
            'date': f"{week.start_date}",
            'timeZone': 'America/New_York',
        },
        'end': {
            'date': f"{week.start_date + datetime.timedelta(days=7)}",
            'timeZone': 'America/New_York',
        },
        }
        service.events().insert(calendarId=CAL_ID, body=new_event).execute()
        print('Event created')


