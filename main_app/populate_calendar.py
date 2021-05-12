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

    # print(desired_week, offered_week)

    # FIND THE 2 MATCHING EVENTS
    desired_event_id = ""
    offered_event_id = ""

    for event in events:
        # print(event["start"]["date"], desired_week.start_date)
        # print(type(event["start"]["date"]), type(desired_week.start_date))

        if event["start"]["date"] == str(desired_week.start_date):
            desired_event_id = event["id"]
            # print(desired_event_id)
        if event["start"]["date"] == str(offered_week.start_date):
            offered_event_id = event["id"]
            # print(offered_event_id)


    # SWAP AND THEN UPDATE GCAL
    if desired_event_id and offered_event_id:

        service.events().update(calendarId=CAL_ID, eventId=desired_event_id, body={"end":{"date":f'{offered_week.start_date + datetime.timedelta(days=7)}'},"start":{"date":f'{offered_week.start_date}'},'summary': f"{offered_week.owner_group}'s Week",}).execute()
        service.events().update(calendarId=CAL_ID, eventId=offered_event_id, body={"end":{"date":f'{desired_week.start_date + datetime.timedelta(days=7)}'},"start":{"date":f'{desired_week.start_date}'},'summary': f"{desired_week.owner_group}'s Week",}).execute()
        print("swapped gcal")
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
            'date': f"{week.start_date + datetime.timedelta(days=7)}",
            'timeZone': 'America/New_York',
        },
        }
        print(new_event)
        service.events().insert(calendarId=CAL_ID, body=new_event).execute()
        print('Event created')


