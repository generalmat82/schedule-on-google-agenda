from datetime import date, datetime
from tkcalendar import Calendar
from tkinter import *
  
import os
import json

def select_vacation(parent:Tk,x,y,fontSize:int):
    top = Toplevel(parent)
    top.title("boo")
    top.focus()
    now = date.today()
    cal = Calendar(top, font=fontSize, selectmode='day', locale='en_US',
        cursor="hand1", year=now.year, month=1, day=1,)
    add_already_selected_date(now, cal)
    cal.pack(fill="both", expand=True)
    Button(top, text="ok", command=lambda top=top,cal=cal,x=x,y=y:add_to_vacation_list(top,cal,x,y)).pack()

def add_already_selected_date(now, cal):
    for i in range(1,len(add_to_vacation_list.vacation)+1):
        for j in range(len(add_to_vacation_list.vacation[f'{i}'])):
            date = datetime(now.year,i,add_to_vacation_list.vacation[f'{i}'][j])
            cal.calevent_create(date,'vacation','vacation')
            cal.tag_config('vacation', background='red', foreground='yellow')
def add_to_vacation_list(top,cal,dateSelectedLabel:Label,selectedDateLabelStr:StringVar):
    selectedDate=cal.selection_get()
    selectedDateLabelStr.set(cal.selection_get())
    top.destroy()
    add_to_vacation_list.vacation[str(selectedDate.month)].append(selectedDate.day)
    print('hello')

add_to_vacation_list.vacation={
    '1' : [],
    '2' : [],
    '3' : [],
    '4' : [],
    '5' : [],
    '6' : [],
    '7' : [],
    '8' : [],
    '9' : [],
    '10' : [],
    '11' : [],
    '12' : []
}

def setup_vacation(parent:Tk,fontSize):
    selectedDateLabelStr=StringVar(parent)
    dateSelectedLabel = Label(parent,text='',textvariable=selectedDateLabelStr,font=fontSize)
    dateSelectedLabel.pack()
    buttonSelect = Button(parent,text='select',command=lambda parent=parent, dateSelectedLabel=dateSelectedLabel,fontSize=fontSize:select_vacation(parent,dateSelectedLabel,selectedDateLabelStr,fontSize),font = fontSize)
    buttonSelect.pack()
    finishButton = Button(parent,text='finish',command=lambda parent=parent,fontSize=fontSize:finish(parent,fontSize),font=fontSize)
    finishButton.pack()

def finish(parent:Tk,fontSize:int):
    for i in range(1,len(add_to_vacation_list.vacation)+1):
        try:
            add_to_vacation_list.vacation[i].sort()
        except:
            continue
    add_vacation_to_a_file()
    return add_to_vacation_list.vacation

def add_vacation_to_a_file():
    add_to_vacation_list.vacation["madeOn"] = str(date.today())
    if os.path.isfile('vacation.txt'):#checks if the vacation.txt file exists
        with open('vacation.txt', 'w') as file:
            file.write("")# wipes the file
            file.write(json.dumps(add_to_vacation_list.vacation))
            # end overwrite file
        # end if del-file
    else:
        with open('vacation.txt', 'w') as file:
            # Comment: 
            file.write(json.dumps(add_to_vacation_list.vacation))
        # end overwrite file

