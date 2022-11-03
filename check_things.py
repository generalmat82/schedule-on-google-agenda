from datetime import date, timedelta
import json

def check_holiday(weeksToBeAdded,dayTodo,now):
    holidayList = holiday_list_maker()
    #----------------------------------------
    datesToSkip = []
    weeksToBeAdded = weeksToBeAdded-1
    totaldays = weeksToBeAdded * 7
    for i in range(0, dayTodo):
        wekday = date.weekday(now)
        if wekday == 5 or wekday == 6: 
            datesToSkip.append(f'{now.year}-{now.month}-{now.day}')
            break
        month = now.month
        for j in (holidayList[str(month)]):
            if j == now.day:
                datesToSkip.append(f'{now.year}-{now.month}-{j}')
                break
        now = now + timedelta(days = 1)
#-------------------------------------------------------------------------------------------------------------------------------
    for i in range(0,totaldays+1):
        wekday = date.weekday(now)
        if wekday == 5 or wekday == 6: 
            datesToSkip.append(f'{now.year}-{now.month}-{now.day}')
            now = now + timedelta(days = 1)
            continue
        month = now.month
        for j in (holidayList[month]):
            if j == now.day: 
                datesToSkip.append(f'{now.year}-{now.month}-{j}')
                break
        now = now + timedelta(days = 1)
    datesToSkip.append(totaldays+dayTodo+1)
    return datesToSkip
#------------------------------------------------------------------------------
def holiday_list_maker():
    with open('vacation.txt', 'r') as file:
    # Comment: 
        holidayList = json.loads(file.readline())
    return holidayList
#===============================================================================================================================

def how_many_days_till_weekend(now,):
    dayTodo=0
    for i in range(0,5):
        check = now + timedelta(days= i)
        weekendCheck = date.weekday(check)
        if weekendCheck == 6 or weekendCheck == 5:
            break
        dayTodo+=1
    return dayTodo

#===============================================================================================================================

def is_skip_needed(dateA,datesToSkip,):
    dateA = f'{dateA.year}-{dateA.month}-{dateA.day}'
    for i in datesToSkip:
        if i == dateA: 
            return False
    return True

#===============================================================================================================================

def remake_schedule():
    with open('schedule.txt', 'r') as f:
        # Comment: 
        schedule = json.loads(f.readline())
    # end readline file
    return schedule
