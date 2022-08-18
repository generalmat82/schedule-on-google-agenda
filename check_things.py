from datetime import *

def check_holiday(weeks_to_be_added,day_todo,now):
    dates_to_skip = []
    holiday_list = {
        '1' : [2, 3, 4, 5, 6, 27],#January
        '2' : [20,],#February
        '3' : [13, 14, 15, 16, 17,], #march
        '4' : [7, 10, 28],#April
        '5' : [22,],#May
        '6' : [5,23, 26, 27, 28, 29, 30], #June
        '7' : [3, 4, 5, 6, 7, 10, 11, 12, 13, 14, 17, 18, 19, 20, 21, 24, 25, 26, 27, 28,], #July
        '8' : [1, 2, 3, 4, 5, 8, 9, 10, 11, 12, 15, 16, 17, 18, 19, 22, 23, 24, 25, 26, 29,],# August
        '9' : [5,], #September
        '10' : [10, 24], #October
        '11' : [25, ], #November
        '12' : [26, 27, 28, 29, 310,] #December
    }
    weeks_to_be_added = weeks_to_be_added-1
    total_days = weeks_to_be_added * 7
    for i in range(0, day_todo):
        wekday = date.weekday(now)
        if wekday == 5 or wekday == 6: 
            dates_to_skip.append(f'{now.year}-{now.month}-{now.day}')
            break
        month = now.month
        for j in (holiday_list[f'{month}']):
            if j == now.day:
                dates_to_skip.append(f'{now.year}-{now.month}-{j}')
                break
        now = now + timedelta(days = 1)
#-------------------------------------------------------------------------------------------------------------------------------
    for i in range(0,total_days+1):
        wekday = date.weekday(now)
        if wekday == 5 or wekday == 6: 
            dates_to_skip.append(f'{now.year}-{now.month}-{now.day}')
            now = now + timedelta(days = 1)
            continue
        month = now.month
        for j in (holiday_list[str(month)]):
            if j == now.day: 
                dates_to_skip.append(f'{now.year}-{now.month}-{j}')
                break
        now = now + timedelta(days = 1)
    dates_to_skip.append(total_days+day_todo+1)
    return dates_to_skip

#===============================================================================================================================

def check_weekend(now,):
    day_todo=0
    for i in range(0,5):
        check = now + timedelta(days= i)
        weekend_check = date.weekday(check)
        if weekend_check == 6 or weekend_check == 5:
            break
        day_todo+=1
    return day_todo

#===============================================================================================================================

def is_skip_needed(date_a,dates_to_skip,):
    date_a = f'{date_a.year}-{date_a.month}-{date_a.day}'
    for i in dates_to_skip:
        if i == date_a: 
            return False
    return True

#===============================================================================================================================

def remake_schedule():
    schedule = {
        'jour_1' : {
            'class1' : {
                'summary' : 'class a',
                'location' : 'class location',
                'description' : 'jour 1 classe 1',
                'start' : {
                    'dateTime' : '2022-08-18T09:15:00',
                    'timeZone' : 'America/Toronto',
                },
                'end': {
                    'dateTime' : '2022-08-18T10:30:00',
                    'timeZone' : 'America/Toronto',
                },
            },
            'class2' : {
                'summary' : 'class b',
                'location' : 'class location',
                'description' : 'jour 1 classe 2',
                'start' : {
                    'dateTime' : '2022-08-18T10:40:00',
                    'timeZone' : 'America/Toronto'
                },
                'end' : {
                    'dateTime' : '2022-08-18T11:55:00',
                    'timeZone' : 'America/Toronto',
                },
            },
            'class3' : {
                'summary' : 'class c',
                'location' : 'class location',
                'description' : 'jour 1 classe 3',
                'start' : {
                    'dateTime' : '2022-08-18T12:50:00',
                    'timeZone' : 'America/Toronto'
                },
                'end' : {
                    'dateTime' : '2022-08-18T14:05:00',
                    'timeZone' : 'America/Toronto'
                },
            },
            'class4' : {
                'summary' : 'class d',
                'location' : 'class location',
                'description' : 'jour 1 classe 4',
                'start' : {
                    'dateTime' : '2022-08-18T14:15:00',
                    'timeZone' : 'America/Toronto'
                },
                'end' : {
                    'dateTime' : '2022-08-18T15:30:00',
                    'timeZone' : 'America/Toronto',
                },
            },
        },
        'jour_2' : {
            'class1' : {
                'summary' : 'class a',
                'location' : 'class location',
                'description' : 'jour 2 classe 1',
                'start' : {
                    'dateTime' : '2022-08-19T09:15:00',
                    'timeZone' : 'America/Toronto',
                },
                'end': {
                    'dateTime' : '2022-08-19T10:30:00',
                    'timeZone' : 'America/Toronto',
                },
            },
            'class2' : {
                'summary' : 'class b',
                'location' : 'class location',
                'description' : 'jour 2 classe 2',
                'start' : {
                    'dateTime' : '2022-08-19T10:48:00',
                    'timeZone' : 'America/Toronto'
                },
                'end' : {
                    'dateTime' : '2022-08-19T11:55:00',
                    'timeZone' : 'America/Toronto',
                },
            },
            'class3' : {
                'summary' : 'class c',
                'location' : 'class location',
                'description' : 'jour 2 classe 3',
                'start' : {
                    'dateTime' : '2022-08-19T12:50:00',
                    'timeZone' : 'America/Toronto'
                },
                'end' : {
                    'dateTime' : '2022-08-19T14:05:00',
                    'timeZone' : 'America/Toronto'
                },
            },
            'class4' : {
                'summary' : 'class d',
                'location' : 'class location',
                'description' : 'jour 2 classe 4',
                'start' : {
                    'dateTime' : '2022-08-19T14:15:00',
                    'timeZone' : 'America/Toronto'
                },
                'end' : {
                    'dateTime' : '2022-08-19T15:30:00',
                    'timeZone' : 'America/Toronto',
                },
            },
        },
        'jour_3' : {
            'class1' : {
            'summary' : 'class a',
            'location' : 'class location',
            'description' : 'jour 3 classe 1',
            'start' : {
                'dateTime' : '2022-08-20T09:15:00',
                'timeZone' : 'America/Toronto',
            },
            'end': {
                'dateTime' : '2022-08-20T10:30:00',
                'timeZone' : 'America/Toronto',
            },
        },
            'class2' : {
                'summary' : 'class b',
                'location' : 'class location',
                'description' : 'jour 3 classe 2',
                'start' : {
                    'dateTime' : '2022-08-20T10:48:00',
                    'timeZone' : 'America/Toronto'
                },
                'end' : {
                    'dateTime' : '2022-08-20T11:55:00',
                    'timeZone' : 'America/Toronto',
                },
            },
            'class3' : {
                'summary' : 'class c',
                'location' : 'class location',
                'description' : 'jour 3 classe 3',
                'start' : {
                    'dateTime' : '2022-08-20T12:50:00',
                    'timeZone' : 'America/Toronto'
                },
                'end' : {
                    'dateTime' : '2022-08-20T14:05:00',
                    'timeZone' : 'America/Toronto'
                },
            },
            'class4' : {
                'summary' : 'class d',
                'location' : 'class location',
                'description' : 'jour 3 classe 4',
                'start' : {
                    'dateTime' : '2022-08-20T14:15:00',
                    'timeZone' : 'America/Toronto'
                },
                'end' : {
                    'dateTime' : '2022-08-20T15:30:00',
                    'timeZone' : 'America/Toronto',
                },
            },
        },
        'jour_4' : {
            'class1' : {
                'summary' : 'class a',
                'location' : 'class location',
                'description' : 'jour 4 classe 1',
                'start' : {
                    'dateTime' : '2022-08-21T09:15:00',
                    'timeZone' : 'America/Toronto',
                },
                'end': {
                    'dateTime' : '2022-08-21T10:30:00',
                    'timeZone' : 'America/Toronto',
                },
            },
            'class2' : {
                'summary' : 'class b',
                'location' : 'class location',
                'description' : 'jour 4 classe 2',
                'start' : {
                    'dateTime' : '2022-08-21T10:48:00',
                    'timeZone' : 'America/Toronto'
                },
                'end' : {
                    'dateTime' : '2022-08-21T11:55:00',
                    'timeZone' : 'America/Toronto',
                },
            },
            'class3' : {
                'summary' : 'class c',
                'location' : 'class location',
                'description' : 'jour 4 classe 3',
                'start' : {
                    'dateTime' : '2022-08-21T12:50:00',
                    'timeZone' : 'America/Toronto'
                },
                'end' : {
                    'dateTime' : '2022-08-21T14:05:00',
                    'timeZone' : 'America/Toronto'
                },
            },
            'class4' : {
                'summary' : 'class d',
                'location' : 'class location',
                'description' : 'jour 4 classe 4',
                'start' : {
                    'dateTime' : '2022-08-21T14:15:00',
                    'timeZone' : 'America/Toronto'
                },
                'end' : {
                    'dateTime' : '2022-08-21T15:30:00',
                    'timeZone' : 'America/Toronto',
                },
            },
        },
    }
    return schedule
