from __future__ import print_function
from datetime import *
import os.path
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from check_things import check_holiday, check_weekend, is_skip_needed, remake_schedule

# If modifying these scopes, delete the file token.json.
SCOPES = ['https://www.googleapis.com/auth/calendar']

#===============================================================================================================================

def setup():
    """Shows basic usage of the Google Calendar API.
    Prints the start and name of the next 10 events on the user's calendar.
    """
    global service
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
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.json', 'w') as token:
            token.write(creds.to_json())

    try:
        service = build('calendar', 'v3', credentials=creds)
        main()
    except HttpError as error:
        print('An error occurred: %s' % error)

#===============================================================================================================================

def add_events():
    global day,schedule
    schedule = remake_schedule()
    for d in range(0,dates_to_skip[-1]):
        date = now + timedelta(days=d)
        if is_skip_needed(date,dates_to_skip,) == True:
            for j in range(1,5):
                day_st = f'{date}T{class_time[f"class_{j}_st"]}'
                day_en = f'{date}T{class_time[f"class_{j}_en"]}'
                schedule[f'jour_{day}'][f'class{j}']['start']['dateTime'] = day_st
                schedule[f'jour_{day}'][f'class{j}']['end']['dateTime'] = day_en
                schedule[f'jour_{day}'][f'class{j}'] = service.events().insert(calendarId='8l00e35lvlr9nk1sbnqbi7tnro@group.calendar.google.com', body=schedule[f'jour_{day}'][f'class{j}']).execute()
                print(f"day {day} class {j} has been added to the calender.")
        else: continue
        day_st = f'{now + timedelta(days=day+1)}T{class_time["class_1_st"]}'
        day_en = f'{now + timedelta(days=day+1)}T{class_time["class_1_en"]}'
        day+=1
        if day == 5: 
            day = 1
            schedule = remake_schedule()

#===============================================================================================================================

def main():
    global now,schedule,class_time,day,day_todo,dates_to_skip
    now = date.today()
    wakday = date.weekday(now)
    if wakday != 6 or wakday != 5:
        if wakday == 6: now + timedelta(days=1)
        elif wakday == 5: now + timedelta(days=2)
    schedule = remake_schedule()
    class_time = {
        'class_1_st' : '09:15:00',
        'class_1_en' : '10:30:00',
        'class_2_st' : '10:40:00',
        'class_2_en' : '11:55:00',
        'class_3_st' : '12:50:00',
        'class_3_en' : '14:05:00',
        'class_4_st' : '14:15:00',
        'class_4_en' : '15:30:00'
    }
    day_todo = check_weekend(now)
#-------------------------------------------------------------------------------------------------------------------------------
    day=int(input('starting on what day: '))
    weeks_to_be_added = int(input('how many weeks added on google agenda: '))
    dates_to_skip = check_holiday(weeks_to_be_added,day_todo,now)
    add_events()

#===============================================================================================================================

if __name__ == '__main__':
    setup()