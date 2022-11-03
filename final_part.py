from __future__ import print_function
from datetime import *
import os.path
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from check_things import check_holiday, how_many_days_till_weekend, is_skip_needed, remake_schedule

# If modifying these scopes, delete the file token.json.
SCOPES = ['https://www.googleapis.com/auth/calendar']

#===============================================================================================================================

def setup(timeForward,classTime,startDay,weeksToBeAdded,calId):
    """
        makes the base of what is nesesary to add the schedule to google calendar.
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
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.json', 'w') as token:
            token.write(creds.to_json())

    try:
        service = build('calendar', 'v3', credentials=creds)
        main(timeForward,classTime,startDay,weeksToBeAdded,service,calId)
    except HttpError as error:
        print('An error occurred: %s' % error)

#===============================================================================================================================

def add_events(service,now:date,classTime:dict,datesToSkip:list,day:int,calId):
    schedule = remake_schedule()
    for d in range(0,datesToSkip[-1]):
        date = now + timedelta(days=d)
        if is_skip_needed(date,datesToSkip,) == True:
            for j in range(1,5):
                dayStart = f'{date}T{classTime["st"][f"class_{j}_st"]}'
                dayEnd = f'{date}T{classTime["en"][f"class_{j}_en"]}'
                schedule[f'day{day}'][f'class{j}']['start']['dateTime'] = dayStart
                schedule[f'day{day}'][f'class{j}']['end']['dateTime'] = dayEnd
                schedule[f'day{day}'][f'class{j}'] = service.events().insert(calendarId=calId, body=schedule[f'day{day}'][f'class{j}']).execute()
                print(f"day {day} class {j} has been added to the calender.")
        else: continue
        dayStart = f'{now + timedelta(days=day+1)}T{classTime["st"]["class_1_st"]}'
        dayEnd = f'{now + timedelta(days=day+1)}T{classTime["en"]["class_1_en"]}'
        day+=1
        if day == 5: 
            day = 1
            schedule = remake_schedule()

#===============================================================================================================================

def main(timeForward:int,classTime:dict,startDay:int,weeksToBeAdded:int,service,calId:str):
    now = date.today()
    now = now + timedelta(days=timeForward)
    WhatWeekDay = date.weekday(now)
    if WhatWeekDay != 6 or WhatWeekDay != 5:
        if WhatWeekDay == 6: now=now + timedelta(days=1)
        elif WhatWeekDay == 5: now=now + timedelta(days=2)
    dayTodo = how_many_days_till_weekend(now)
    #------------------------------------------------------------------------------
    datesToSkip = check_holiday(weeksToBeAdded,dayTodo,now)
    add_events(service,now,classTime,datesToSkip,startDay,calId)
#===============================================================================================================================