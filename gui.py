import json
import os
import re
from datetime import date
from random import randint
from tkinter import *
from tkinter import ttk
from tkinter import filedialog
from tkinter.messagebox import showerror

from tkcalendar import Calendar

import time_picker
from final_part import setup
from notificationChoice import notif_screen
from vacationselection import setup_vacation

"""
todo change size of things
todo make sure everything works perfectly
todo make code cleaner
todo add more comments
todo fix bugs
    /todo/ description not entering.
    /todo/ focus out of things when "changing" of window
    /todo/ 12h time picker at 12 pm puts it at midnight instead of midday.
/todo/ verify that every info needed has been puted before adding to the calendar
    /todo/ aka the amount of weeks to add,day on which we are starting and the calendar id.
/todo/ must add the schedule to the calendar
/todo/ have to add a calendar id input
/todo/ show the already made schedule, and vacation if it exist
todo add a thing to add a credential file/put the text of the credential file

    ¦¦¦¦
        separation between big parts of code
    ====
        separation between the parts of its biger part
    ~~~~
        separation between every fonction
    ----
        separates a parts of a function
"""
# ¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦

# *********************************for start setup********************************

def setup_main(fenetre: Tk):
    """
    Purpose: to make the basic setup of the gui with the tabs
    Parameters:
        fentre: tkinter.Tk()
        Returns:
            None
    """
    styleTabSelector = ttk.Style()
    styleTabSelector.configure('TNotebook.Tab', font=("segoe UI", 13))
    tabSelector = ttk.Notebook(fenetre)  # for making the tabs
    # ------------------------------------------------------
    # *tab for adding the stuff to the calendar
    #-----------------------------------------------
    #* frame for the tab to put everything on the calendar
    tabAddToCallendar = Frame(tabSelector)
    tabSelector.add(tabAddToCallendar, text='add to calendar', padding=5)
    # ------------------------------------------------------
    # *tab for the making of the schedule
    #* frame for the tab to make schedule
    tabForMakingSchedule = Frame(tabSelector)
    tabSelector.add(tabForMakingSchedule,
                    text='make the schedule', padding=5)  # adds the tab
    # ------------------------------------------------------
    # *tab for the vacation
    tabVacationSelect = Frame(tabSelector)
    tabSelector.add(tabVacationSelect, text='Vacation selection', padding=5)
    tabSelector.pack(expand=1, fill="both")
    #----------------------------------------------------
    # * tab for the documentation
    # tabDocumentation = Frame(tabSelector)
    # tabSelector.add(tabDocumentation, text='documentation', padding=5)
    # tabSelector.pack(expand=1, fill="both")
    # ---------------------------------------------------------------------
    # *add the gui for each tabs
    add_calendar_start(tabAddToCallendar)
    making_new_schedule(tabForMakingSchedule)
    select_vacation_start(tabVacationSelect)
    # documentation_start(tabDocumentation)

# ¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦

# ********************************************schedule making***********************************************

# ******************************start new schedule******************************

def making_new_schedule(parent: Frame):
    """
        Purpose: makes the base of the new schedule screen
        Parameters:
        parent: tkinter.Tk()
        Returns:
            None
    """
    doYouWishToContinue = Button(parent, text='make a new schedule', font=(
        "segoe UI", 13))  # makes a button to start making a new schedule
    doYouWishToContinue.grid(column=1, row=1)
    if os.path.isfile('schedule.txt'):
        # if theres an already existing schedule it runs a function
        scheduleTab = get_schedule_tab_matrix(parent)
    # ------------------------------------------------------------------------------------------
    try:
        doYouWishToContinue.config(command=lambda parent=parent, doYouWishToContinue=doYouWishToContinue,
                                   scheduleTab=scheduleTab: amount_days_class(parent, doYouWishToContinue, scheduleTab))
    except:
        doYouWishToContinue.config(
            command=lambda parent=parent, doYouWishToContinue=doYouWishToContinue: amount_days_class(parent, doYouWishToContinue))

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

def get_schedule_tab_matrix(parent: Frame):
    """
        Purpose: makes the matrix for showing the schedule on screen
        Parameters:
            parent: tkinter.Tk()
            Returns:
                canvas
    """
    shadesOfGray = ['#B2BEB5', '#848482', '#54626F', '#625D5D', '#36454F',
                    '#A9A9A9', '#555555', '#696969', '#808080', '#B6B6B4', '#5C5858']
    # *obtention of the schedule
    with open('schedule.txt', 'r') as f:  # opens the schedule.txt file and read the schedule
        schedule = json.loads(f.readline())  # gets the schedule
    dayAmount = schedule["numDays"]  # takes the amount of days
    # takes the amount of classes a day
    classAmount = schedule['numClassPerDay']
    # ------------------------------------------------------------------------------
    # * this area is to make the table base so only day number and class is in it rest empty stings
    # makes the top column with the day
    scheduleTabInfo = [f'day {i}' for i in range(dayAmount+1)]
    scheduleTabInfo[0] = ' '  # makes the first cell empty
    # makes the dictanary the table will be in
    scheduleTab = {'inf': scheduleTabInfo}
    # ----------------------------------
    for c in range(1, classAmount+1):
        # for the first cell of every row with the class number in it
        scheduleTabClass = [f'class {c}']
        scheduleTabClassInfo = ['' for d in range(1, classAmount+1)]
        for i in range(len(scheduleTabClassInfo)):
            scheduleTabClass.append(scheduleTabClassInfo[i])
        scheduleTab[f'{scheduleTabClass[0]}'] = scheduleTabClass
    # --------------------------------------------------------------------------------
    # * this area is to add the info to each empty cell
    for c in range(1, classAmount+1):
        for d in range(1, dayAmount+1):
            classSummary = schedule[f'day{d}'][f'class{c}']['summary']
            classLocation = schedule[f'day{d}'][f'class{c}']['location']
            classDescription = schedule[f'day{d}'][f'class{c}']['description']
            classText = f'{classSummary}\n{classDescription}\n{classLocation}'
            scheduleTab[f'class {c}'][d] = classText
    # --------------------------------------------------------------
    # * adds the schedule to the screen
    scheduleTableCanvas = Canvas(parent, background="black")
    scheduleTableCanvas.grid(column=1, row=2)
    for r in range(classAmount):
        scheduleTableCanvas.rowconfigure(r, weight=1)
    for c in range(dayAmount):
        scheduleTableCanvas.columnconfigure(c, weight=1)
    # ---------------------------------------------------------------
    scheduleTabLabels = scheduleTab.copy()
    # makes the labels for top column
    for i in range(len(scheduleTabLabels['inf'])):
        scheduleTabLabels['inf'][i] = Label(
            scheduleTableCanvas, text=scheduleTabLabels['inf'][i], font=("seogoe UI", 12),)
        scheduleTabLabels['inf'][i].grid(
            row=0, column=i, sticky='NSEW', padx=1, pady=1)
    for c in range(1, len(scheduleTabLabels)):  # makes the labels for the rest
        for d in range(len(scheduleTabLabels[f'class {c}'])):
            scheduleTabLabels[f'class {c}'][d] = Label(scheduleTableCanvas, font=(
                "seogoe UI", 10), text=scheduleTabLabels[f'class {c}'][d], border=0, bg=shadesOfGray[int(d+c/2+randint(0, 4))])
            scheduleTabLabels[f'class {c}'][d].grid(
                row=c, column=d, sticky='NSEW', padx=1, pady=1)
    return scheduleTableCanvas

# ===============================================================================================================================

# ********************************amount of days and classes in each days in the schedule page **********************************

def amount_days_class(parent: Tk, doYouWishToContinue: Button, scheduleTab: Canvas = None):
    """
    Purpose: takes the amount of days in the schedule and
    the amount of classes per day
    Parameters:
        parent: tkinter.Tk(),
        doYouWishToContinue: Button
        scheduleTab: canvas
    """
    #*deletes the start page of the prosses
    doYouWishToContinue.grid_forget()
    doYouWishToContinue.forget()
    try:
        scheduleTab.grid_forget()
        scheduleTab.forget()
    except:
        print("hi")
    # ----------------------------------------------------------
    # *amount of days in schedule box and label
    numDaysBox = Spinbox(  # to select the amount of days
        parent, textvariable=numDaysStr, from_=0, to=10000, font=("segoe UI", 13), state='readonly')
    numDaysBox.grid(column=0, row=1, padx=1, pady=1)
    numDaysLabel = Label(  # says what the input is
        parent, text='amount of days in the schedule:', font=("segoe UI", 13))
    numDaysLabel.grid(column=0, row=0)
    # ----------------------------------------------------------
    # *amount of classes in schedule box and label
    numClassesLabel = Label(  # says what the input is for
        parent, text='amount of classes per day:', font=("segoe UI", 13))
    numClassesLabel.grid(column=1, row=0)
    numClassesBox = Spinbox(  # input for the amount of classes per day
        parent, textvariable=numClassStr, from_=0, to=10000, font=("segoe UI", 13), state='readonly')
    numClassesBox.grid(column=1, row=1)
    # ------------------------------------------------------
    # *continue button
    continueButton = Button(parent, text='Continue', font=("segoe UI", 13))
    continueButton.config(  # button to continue on the schedule creation
        command=lambda a=numDaysBox, b=numDaysLabel, c=numClassesBox, d=numClassesLabel, e=continueButton, parent=parent: del_amount_day_class(
            a, b, c, d, e, parent)
    )
    continueButton.grid(column=2, row=2,)

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

def del_amount_day_class(
    numDaysBox: Spinbox, numDaysLabel: Label, numClassesBox: Spinbox, numClassesLabel: Label, continueButton: Button, parent: Tk
):
    """
    Purpose: to wipe the screen for the next step of the schedule prosses after taking the amount of days and classes per day
    """
    numDays = int(numDaysStr.get()
                  )  # to get the amount of days in the schedule
    classPerDay = int(numClassStr.get())  # to get the amount of class per day
    # --------------------------------------------------------------------------
    numDaysBox.grid_forget()
    numDaysLabel.grid_forget()
    numClassesBox.grid_forget()
    numClassesLabel.grid_forget()
    continueButton.grid_forget()
    numDaysBox.forget()
    numDaysLabel.forget()
    numClassesBox.forget()
    numClassesLabel.forget()
    continueButton.forget()
    parent.focus()
    # --------------------------------------------------------------------------
    class_time_start_end(parent, numDays, classPerDay)

# ===============================================================================================================================

# *********************************takes start and end time for each class during the day********************************

def class_time_start_end(parent: Tk = None, numDays: int = None, classPerDay: int = None):
    """
    Purpose: to get the start and end time of every classes
    """
    # *to make the base of the list
    print('test')
    add_class.wholeSchedule = {f'day{i}': {f'class{i}': {} for i in range(
        1, classPerDay+1)} for i in range(1, numDays+1)}
    add_class.wholeSchedule["numDays"] = numDays
    add_class.wholeSchedule["numClassPerDay"] = classPerDay
    class_time_start_end.classTimeStartEndList = {'st': {f'class_{i}_st': '' for i in range(
        1, classPerDay+1)}, 'en': {f'class_{i}_en': '' for i in range(1, classPerDay+1)}}
    # --------------------------------------------------------------------------------------------------------------------------------------
    # *information label
    infoLabel = Label(  # Label with the info of what day and class we are doing at the moment
        parent, text=f"time of the class in the {verif_continue.classTimeTaken} period:", font=("segoe UI", 13)
    )
    infoLabel.grid(column=0, row=0)
    # -------------------------------------------------------------------------------------------------------------------------------
    # *to add the start time of the class
    classStartTimeStr = StringVar(parent, value="")
    classStartTimeButton = Button(  # add the button to select the class start time
        parent, text='start time selection', command=lambda parent=parent, x=classStartTimeStr: start_time_select(parent, x), font=("segoe UI", 13)
    )
    classStartTimeButton.grid(column=1, row=3)
    # -------------------------------------------------------------------------------------------------------------------------------
    # *label for showing what time was selected for the start time of the class
    classStartTimeLabel = Label(  # label
        parent, textvariable=classStartTimeStr, font=("segoe UI", 13)
    )
    classStartTimeLabel.grid(column=2, row=3)
    # -------------------------------------------------------------------------------------------------------------------------------
    # *to add the end time of the class
    classEndTimeLabelStr = StringVar(parent, value="")
    classEndTimeButton = Button(  # add the button to select the class end time
        parent, text='end time selection', command=lambda parent=parent, x=classEndTimeLabelStr: end_time_select(parent, x), font=("segoe UI", 13)
    )
    classEndTimeButton.grid(column=1, row=4)
    # -------------------------------------------------------------------------------------------------------------------------------
    # *Label for showing what time was selected for the start time of the class
    classEndTimeLabel = Label(  # label
        parent, textvariable=classEndTimeLabelStr, font=("segoe UI", 13)
    )
    classEndTimeLabel.grid(column=2, row=4)
    # -------------------------------------------------------------------------------------------------------------------------------
    # *to traceing the time variables
    classEndTimeLabelStr.trace_add("write", lambda nm, idx, mode,  # to execute a command when the variable is changed
                                   x=classStartTimeStr, y=classEndTimeLabelStr, z=infoLabel,
                                   a=classPerDay, c=classStartTimeButton, d=classStartTimeLabel,
                                   e=classEndTimeButton, f=classEndTimeLabel, parent=parent: verif_continue(parent, x, y, z, a, c, d, e, f)
                                   )
    classStartTimeStr.trace_add("write", lambda nm, idx, mode,  # to execute a command when the variable is changed
                                classStartTimeStr=classStartTimeStr, classEndTimeLabelStr=classEndTimeLabelStr, infoLabel=infoLabel,
                                classPerDay=classPerDay, classStartTimeButton=classStartTimeButton, classStartTimeLabel=classStartTimeLabel,
                                classEndTimeButton=classEndTimeButton, classEndTimeLabel=classEndTimeLabel, parent=parent:
                                verif_continue(
                                    parent, classStartTimeStr, classEndTimeLabelStr, infoLabel, classPerDay,
                                    classStartTimeButton, classStartTimeLabel, classEndTimeButton, classEndTimeLabel
                                )
                                )

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

def del_period_time_taking(
    parent: Tk = None, infoLabel: Label = None, classStartTimeButton: Button = None, classEndTimeButton: Button = None,
    classStartTimeLabel: Label = None, classEndTimeLabel: Label = None, continueButton: Button = None
):
    """
    Purpose: to wipe the screen for the next step of the schedule prosses after taking the time of every classes 
    """
    infoLabel.grid_forget()
    infoLabel.forget()
    classStartTimeButton.grid_forget()
    classStartTimeButton.forget()
    classEndTimeButton.grid_forget()
    classEndTimeButton.forget()
    classStartTimeLabel.grid_forget()
    classStartTimeLabel.forget()
    classEndTimeLabel.grid_forget()
    classEndTimeLabel.forget()
    continueButton.grid_forget()
    continueButton.forget()
    parent.focus()
    # --------------------------------
    make_rest_of_schedule(parent)

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

def verif_continue(
    parent: Tk = None, classStartTimeStr: StringVar = None, classEndTimeLabelStr: StringVar = None, infoLabel: Label = None,
    classPerDay: int = None, classStartTimeButton: Button = None, classStartTimeLabel: Label = None,
    classEndTimeButton: Button = None, classEndTimeLabel: Label = None
):
    """
        purpose: to verify that both start time and end time are selected before showing the continue button
    """
    if classEndTimeLabelStr.get() != "" and classStartTimeStr.get() != "":  # verify that both time has been inputed
        # creates the continue Button
        continueButton = Button(parent, text="continue")
        continueButton.config(command=lambda  # puts the command for the continue Button
                              parent=parent, classStartTimeStr=classStartTimeStr, classEndTimeLabelStr=classEndTimeLabelStr, classPerDay=classPerDay,
                              infoLabel=infoLabel, continueButton=continueButton, classStartTimeButton=classStartTimeButton,
                              classStartTimeLabel=classStartTimeLabel, classEndTimeButton=classEndTimeButton, classEndTimeLabel=classEndTimeLabel:
                              next_class(
                                  parent, classStartTimeStr, classEndTimeLabelStr, classPerDay, infoLabel, continueButton,
                                  classStartTimeButton, classStartTimeLabel, classEndTimeButton, classEndTimeLabel
                              )
                              )
        continueButton.grid(column=6, row=6)
        print("potatoo🥔")
    print("hi")

verif_continue.classTimeTaken = 1

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

def next_class(
    parent: Tk = None, classStartTimeStr: StringVar = None, classEndTimeLabelStr: StringVar = None, classPerDay: int = None,
    infoLabel: Label = None, continueButton: Button = None, classStartTimeButton: Button = None, classStartTimeLabel: Label = None,
    classEndTimeButton: Button = None, classEndTimeLabel: Label = None
):
    """
        purpose: to make so you can input the next class start and end time
    """
    print("potatoo🥔")
    #------------------------------------------------------------------------------
    #* adds the dtart and end times to the list of time for heach classes
    class_time_start_end.classTimeStartEndList["st"][f"class_{verif_continue.classTimeTaken}_st"] = classStartTimeStr.get(
    )
    class_time_start_end.classTimeStartEndList["en"][f"class_{verif_continue.classTimeTaken}_en"] = classEndTimeLabelStr.get(
    )
    #------------------------------------------------------------------------------
    #* sets up for the taking of the next class
    verif_continue.classTimeTaken += 1
    infoLabel.config(  # changes the information label for the next class
        text=f"time of the class in the {verif_continue.classTimeTaken} period:")
    classEndTimeLabelStr.set("")
    classStartTimeStr.set("")
    continueButton.grid_forget()
    parent.focus()
    #------------------------------------------------------------------------------
    #* if the class we are doing is over the amount of class we have we will go to another function
    if verif_continue.classTimeTaken >= classPerDay+1:
        with open('time.txt', 'w') as f:
            f.write(json.dumps(class_time_start_end.classTimeStartEndList))
        del_period_time_taking(parent, infoLabel, classStartTimeButton,
                               classEndTimeButton, classStartTimeLabel, classEndTimeLabel, continueButton)

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

def end_time_select(parent: Tk = None, x: StringVar = None):
    """
        purpose: to select the time of end of the class
    """
    endTimeWindow = Toplevel(parent)  # creates the window for the selection
    endTimeWindow.geometry("750x250")
    endTimeWindow.title("end of class time selection")
    doneButton = Button(endTimeWindow, text='finished', )
    timeSelector = time_picker.setup(
        endTimeWindow, doneButton)  # gets the time selector
    doneButton.config(command=lambda timeSelector=timeSelector,
                      endTimeWindow=endTimeWindow, x=x: add_end_time(timeSelector, endTimeWindow, x))
    endTimeWindow.focus()

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

def add_end_time(timeSelector: time_picker.TimeSelection = None, endTimeWindow: Toplevel = None, classEndTimeLabelStr: StringVar = None):
    """
        purpose: to confirm the selected end time for the class
    """
    end_time = timeSelector.make_time()  # gets the end time
    endTimeWindow.destroy()  # closes the window to select the end time
    classEndTimeLabelStr.set(end_time)

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

def start_time_select(parent: Tk = None, x: StringVar = None):
    """
        purpose: to select the time of start of the class
    """
    startTimeWindow = Toplevel(parent)  # creates the window for the selection
    startTimeWindow.geometry("750x250")
    startTimeWindow.title("Start of class time selection")
    doneButton = Button(startTimeWindow, text='finished')
    timeSelector = time_picker.setup(
        startTimeWindow, doneButton)  # gets the time selector
    doneButton.config(command=lambda x=x, startTimeSelector=timeSelector,
                      startTimeWindow=startTimeWindow: add_start_time(startTimeSelector, startTimeWindow, x))
    startTimeWindow.focus()

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

def add_start_time(timeSelector: time_picker.TimeSelection = None, startTimeWindow: Toplevel = None, classStartTimeStr: StringVar = None):
    """
        to confirm the selected start time for the class
    """
    startTime = timeSelector.make_time()  # gets the start time
    startTimeWindow.destroy()  # closes the window to select the start time
    classStartTimeStr.set(startTime)
    return startTime

# ======================================================================================================================================

# *********************************makes the whole schedule things********************************

def make_rest_of_schedule(parent: Tk = None):
    """
        purpose: to make the rest of the schedule.
    """
    make_rest_of_schedule.classNumDoing = 1
    make_rest_of_schedule.dayNumDoing = 1
    # -------------------------------------------------------------------------------------------------------------------------------
    # *label that tells which class of what day
    infoLabelStr = StringVar(value="day 1\nclass 1")
    infoLabel = Label(parent, textvariable=infoLabelStr,
                      font=("segoe UI", 13))  # information Label
    infoLabel.grid(column=0, row=0)
    # -------------------------------------------------------------------------------------------------------------------------------
    # *box for the name of the class
    nameOfClassStr = StringVar(value="name of class")
    nameOfClassEntry = Entry(  # entry for the name of the class
        parent, textvariable=nameOfClassStr, width=20, font=("segoe UI", 13))
    nameOfClassEntry.grid(column=2, row=2, ipadx=5, ipady=5, padx=5, pady=5)
    nameOfClassStr.trace_add("write", lambda nm, idx, mode, nameOfClassStr=nameOfClassStr,  # to exectute a function when the entry is modified
                             og='name of class', x=1: pre_remove_placeHolder(og, x, nameOfClassStr)
                             )
    # -------------------------------------------------------------------------------------------------------------------------------
    # *Button to sets notifications/reminders
    notifList = []
    setNotifButton = Button(parent, text='set notifications', command=lambda parent=parent,  # button to set the reminders
                            notifList=notifList: notif_screen(parent, notifList), font=("segoe UI", 13)
                            )
    setNotifButton.grid(column=5, row=0)
    # -------------------------------------------------------------------------------------------------------------------------------
    # *box for the location of the class
    locationEntryStr = StringVar(parent, value='location of the class')
    locationEntry = Entry(  # entry to set the location of the class
        parent, textvariable=locationEntryStr, font=("segoe UI", 13), width=20
    )
    locationEntry.grid(column=2, row=3, ipadx=5, ipady=5, padx=5, pady=5)
    locationEntryStr.trace_add("write", lambda nm, idx, mode, locationEntryStr=locationEntryStr,  # to exectute a function when the box is modified
                               og='location of the class', x=2: pre_remove_placeHolder(og, x, locationEntryStr)
                               )
    # -------------------------------------------------------------------------------------------------------------------------------
    # *box for the description
    desciptionText = Text(parent, width=20, height=10, font=(
        "segoe UI", 13))  # text for the description of the class
    desciptionText.grid(column=2, row=4, ipadx=5, ipady=5, padx=5, pady=5)
    #* puts the placeholder for the descriptionText
    desciptionText.insert('1.0', 'description of the class')
    desciptionText.bind('<Key>', lambda nm, og='description of the class',  # checks for edit of the box to execute a function
                        x=3, y=desciptionText: pre_remove_placeHolder(original=og, entryNum=x, widget=y)
                        )
    # -------------------------------------------------------------------------------------------------------------------------------
    # *button to confirm what has been added
    confirmButton = Button(parent, text='Confirm', font=(
        "segoe UI", 13),)  # confirm button
    confirmButton.config(command=lambda  # adds the function to execute on press
                         infoLabelStr=infoLabelStr, nameOfClassStr=nameOfClassStr, notifList=notifList, locationEntryStr=locationEntryStr,
                         infoLabel=infoLabel, nameOfClassEntry=nameOfClassEntry,
                         setNotifButton=setNotifButton, locationEntry=locationEntry, desciptionText=desciptionText, confirmButton=confirmButton, parent=parent:
                         add_class(infoLabelStr, nameOfClassStr, notifList, locationEntryStr, infoLabel,
                                   nameOfClassEntry, setNotifButton, locationEntry, desciptionText, confirmButton, parent)
                         )
    confirmButton.grid(column=0, row=5)

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

def pre_remove_placeHolder(original: str, entryNum: int, thingStr: StringVar = None, widget: Text = None):
    """
    purpose: for removing the placeholder on the entrys
    Parameters:
        original: str(original string of the entry)
        entryNum: int(entry number of the entry
            • 1 = nameOfClassEntry
            • 2 = locationEntry
            • 3 = descriptionText
            )
        thingStr: StringVar(stringvar of the entry)
        widget: Text(text widget for the desciptionText)
    """
    if entryNum == 1 and not pre_remove_placeHolder.skip1:
        remove_placeholder(thingStr, original)
        pre_remove_placeHolder.skip1 = True
    elif entryNum == 2 and not pre_remove_placeHolder.skip2:
        remove_placeholder(thingStr, original)
        pre_remove_placeHolder.skip2 = True
    elif entryNum == 3 and not pre_remove_placeHolder.skip3:
        widget.delete(1.0, END)
        pre_remove_placeHolder.skip3 = True
        return widget
    elif entryNum == 4 and not pre_remove_placeHolder.skip4:
        remove_placeholder(thingStr, original)
        pre_remove_placeHolder.skip4 = True
# ----------------------------------------------------------------
pre_remove_placeHolder.skip1 = False
pre_remove_placeHolder.skip2 = False
pre_remove_placeHolder.skip3 = False
pre_remove_placeHolder.skip4 = False

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

def remove_placeholder(thingStr: StringVar, original: str):
    """
        purpose: remove placeholder from text
    """
    print("potatoo")
    x = thingStr.get()
    for i in range(x.count("", 0)-1):
        try:
            if original[i] == x[i]:
                continue
            else:
                y = x[i]
                thingStr.set(y)
                break
        except:
            y = x[i]
            thingStr.set(y)
            break
    return thingStr

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

def add_class(
        infoLabelStr: StringVar = None, nameOfClassStr: StringVar = None, notifList: list = None, locationEntryStr: StringVar = None,
        infoLabel: Label = None, nameOfClassEntry: Entry = None, setNotifButton: Button = None, locationEntry: Entry = None,
        desciptionText: Text = None, confirmButton: Button = None, parent: Tk = None):
    """
        purpose: add a class to the schedule list
    """
    print("potatoo🥔")
    #* verify that all the info required was entered if it isint it will show an error and stop the function
    if not pre_remove_placeHolder.skip1 or not pre_remove_placeHolder.skip2 or not pre_remove_placeHolder.skip3:
        showerror("invalid insert", "Required information not entered\nOr certain information has not been entered.\nRequired information:\n•Name of the class\n•Location\n•Description")
        return
    #-----------------------------------------------------------
    #* gets the text out of the desciptionText
    desciptionTextStr = desciptionText.get(1.0, END)
    #-----------------------------------------------------------
    #* verify if a notification setting was entered if there was it'll make the list for it 
    if len(notifList) >= 1:
        print("I love singing fwend!(as a friend)")
        reminderListFull = {
            'useDefault': False,
            'overides': [
                notifList
            ]
        }
    else:
        reminderListFull = {'useDefault': True}
    # ------------------------------------------------------------------------------------
    #* makes the list for the class
    classList = {
        'summary': nameOfClassStr.get(),
        'location': locationEntryStr.get(),
        'description': desciptionTextStr,
        'start': {
            'start': class_time_start_end.classTimeStartEndList['st'][f'class_{make_rest_of_schedule.classNumDoing}_st'],
            'timeZone': 'America/Toronto',
        },
        'end': {
            'end': class_time_start_end.classTimeStartEndList['en'][f'class_{make_rest_of_schedule.classNumDoing}_en'],
            'timeZone': 'America/Toronto',
        },
        'reminders': reminderListFull
    }
    # ---------------------------------------------------------------------------------------------
    #* adds the class to the full schedule
    add_class.wholeSchedule[f'day{make_rest_of_schedule.dayNumDoing}'][
        f'class{make_rest_of_schedule.classNumDoing}'] = classList
    #--------------------------------------------------------------------------------------
    #* if not the last class of the day it will reset for the next class
    if make_rest_of_schedule.classNumDoing != add_class.wholeSchedule['numClassPerDay']:
        parent.focus()
        make_rest_of_schedule.classNumDoing += 1
        locationEntryStr.set('location of the class')
        notifList.clear()
        nameOfClassStr.set('name of the class')
        desciptionText.delete(1.0, END)
        desciptionText.insert('1.0', 'description of the class')
        pre_remove_placeHolder.skip1 = False
        pre_remove_placeHolder.skip2 = False
        pre_remove_placeHolder.skip3 = False
    # ----------------------------------------------------------------------------------------------
    #*if it is the last class it'll check of its the last class it will reset for the first class of the first day
    else:
        make_rest_of_schedule.classNumDoing = 1
        if make_rest_of_schedule.dayNumDoing != add_class.wholeSchedule["numDays"]:
            #*if its not the last day itll reset to the next day first class
            make_rest_of_schedule.dayNumDoing += 1
            locationEntryStr.set('location of the class')
            notifList.clear()
            nameOfClassStr.set('name of the class')
            desciptionText.delete(1.0, END)
            desciptionText.insert('1.0', 'description of the class')
            pre_remove_placeHolder.skip1 = False
            pre_remove_placeHolder.skip2 = False
            pre_remove_placeHolder.skip3 = False
            parent.focus()
        else: #*if it is the last class itll remove everyrthing
            clear_make_whole_schedule(infoLabel, nameOfClassEntry, setNotifButton,
                                      locationEntry, desciptionText, confirmButton, parent)
    infoLabelStr.set(
        f'day {make_rest_of_schedule.dayNumDoing}\nclass {make_rest_of_schedule.classNumDoing}')
add_class.wholeSchedule = {}

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

def clear_make_whole_schedule(infoLabel: Label = None, nameOfClassEntry: Entry = None, setNotifButton: Button = None, locationEntry: Entry = None,
                              desciptionText: Text = None, confirmButton: Button = None, parent: Tk = None):
    """
        purpose: to clear the screen
    """
    print("potatoo")
    infoLabel.grid_forget()
    infoLabel.forget()
    # -------------------------------------------------------------------
    nameOfClassEntry.grid_forget()
    nameOfClassEntry.forget()
    # -------------------------------------------------------------------
    setNotifButton.grid_forget()
    setNotifButton.forget()
    # -------------------------------------------------------------------
    locationEntry.grid_forget()
    locationEntry.forget()
    # -------------------------------------------------------------------
    desciptionText.grid_forget()
    desciptionText.forget()
    # -------------------------------------------------------------------
    confirmButton.grid_forget()
    confirmButton.forget()
    # --------------------------------------------------------------------
    confirm_schedule(parent)

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

def confirm_schedule(parent: Tk = None):
    """
        Purpose: to show that the schedule has been created
    """
    print('hello')
    with open('schedule.txt', 'w') as f:
        f.write(json.dumps(add_class.wholeSchedule))
    making_new_schedule(parent)

# ¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦

# *****************************to select what day are a vacation**********************


def select_vacation_start(parent: Frame):
    """
        Purpose: makes the base of the selection menu screen
    """
    #* makes the button to make a new vacation list
    doYouWishToContinue = Button(
        parent, text='select all vacations', font=("segoe UI", 13))
    doYouWishToContinue.grid(column=1, row=1)
    #-----------------------------------------------------------------
    #* makes a calendar to show the selected days:
    now = date.today()
    cal = Calendar(parent, font=("segoe UI", 13), selectmode='day', locale='en_US',
                   cursor="hand1", year=now.year, month=now.month, day=now.day,)
    cal.grid(column=2, row=2)
    #----------------------------------------------------------------
    #* adds the vacation to the calendar
    if os.path.isfile('vacation.txt'):
        # Comment:
        with open('vacation.txt', 'r') as f:
            # Comment:
            vacation = json.loads(f.readline())
        # end readline file
        madeOnYear, madeOnMonth, madeOnDay = (vacation["madeOn"].split('-', 3))
        cal.tag_config('vacation', background='red', foreground='yellow')

        for i in range(int(madeOnMonth), len(vacation)):
            for j in (vacation[str(i)]):
                dateEvent = date(int(madeOnYear), i, j)
                cal.calevent_create(dateEvent, 'vacation', 'vacation')
        for i in range(1, int(madeOnMonth)):
            for j in (vacation[str(i)]):
                dateEvent = date(int(madeOnYear)+1, i, j)
                cal.calevent_create(dateEvent, 'vacation', 'vacation')
    # end if file
    doYouWishToContinue.config(command=lambda parent=parent, doYouWishToContinue=doYouWishToContinue,
                               cal=cal: vacation_selection(parent, doYouWishToContinue, cal))
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~


def vacation_selection(parent: Tk, doYouWishToContinue: Button, cal):
    """
        Purpose: removes the base menu and puts the vacation selection menu
    """
    doYouWishToContinue.grid_forget()
    doYouWishToContinue.forget()
    cal.grid_forget()
    cal.forget()
    setup_vacation(parent, ("segoe UI", 13))

# ¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦

# *********************************adds the stuff to your google calendar********************************


def add_calendar_start(parent: Frame):
    """
        Purpose: Makes the base of the screen to add the schedule to the calendar
    """
    doYouWishToContinue = Button(
        parent, text='add schedule to calendar', font=("segoe UI", 13))
    doYouWishToContinue.grid(column=2, row=2)
    doYouWishToContinue.config(command=lambda parent=parent,
                               doYouWishToContinue=doYouWishToContinue: layout_adding_to_calendar(parent, doYouWishToContinue))

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~


def layout_adding_to_calendar(parent: Tk, doYouWishToContinue: Button):
    """
        purpose: menu to add the schedule to the calendar
    """
    print('potatoo')
    doYouWishToContinue.grid_forget()
    doYouWishToContinue.forget()
    if not os.path.isfile('schedule.txt'):
        showerror(
            "No schedule", "Sorry but not schedule has been found.\nPlease make one and try again.")
    # ----------------------------------------------------------------------------
    # ********************amount of weeks to add to the calendar****************
    WeekToAddLabel = Label(
        parent, text='amount of week to add', font=("segoe UI", 13))
    WeekToAddLabel.grid(column=0, row=1, ipadx=5, ipady=5, padx=5, pady=5)
    # ---------------------------------------------------------
    amountWeekToAddStr = StringVar(parent, value=0)
    amountWeekToAddSpinbox = Spinbox(parent, textvariable=amountWeekToAddStr,  # box to set the amount of weeks to add to the schedule
                                     from_=1, to=10000, font=("segoe UI", 13), wrap=True, width=10)  # ,state='readonly')
    amountWeekToAddSpinbox.grid(
        column=2, row=1, ipadx=2, ipady=2, padx=5, pady=5)
    amountWeekToAddStr.trace_add('write', lambda nm, idx, mode, whichThing='amountWeek',
                                 amountWeekToAddStr=amountWeekToAddStr: required_info_entered(whichThing, amountWeekToAddStr))
    # -----------------------------------------------------------------------------
    # *******************amount of days to skip forward****************
    skipFowrwardLabel = Label(
        parent, text='days to skip forward', font=("segoe UI", 13))
    skipFowrwardLabel.grid(column=0, row=2, ipadx=5, ipady=5, padx=5, pady=5)
    # ----------------------------------------------------------------
    amountOfDayToSkipForwardStr = StringVar(parent, value='0')
    skipForwardSpinbox = Spinbox(parent, textvariable=amountOfDayToSkipForwardStr, from_=0, to=10000, font=(
        "segoe UI", 13), wrap=True, width=10)  # box to set the skip forward days amount
    skipForwardSpinbox.grid(column=2, row=2, ipadx=2, ipady=2, padx=5, pady=5)
    # ----------------------------------------------------------------------------
    # ******************the day of the schedule on which we are starting*****************
    startingDayLabel = Label(
        parent, text='day of schedule you are starting.', font=("segoe UI", 13))
    startingDayLabel.grid(column=0, row=3, ipadx=5, ipady=5, padx=5, pady=5)
    # --------------------------------------------------------------
    startingDayStr = StringVar(parent, value='1')
    try:
        startingDaySpinbox = Spinbox(parent, textvariable=startingDayStr, from_=1, to=add_class.wholeSchedule["numDays"], font=(
            "segoe UI", 13), width=10)  # box to set the day we are starting
    except:
        startingDaySpinbox = Spinbox(parent, textvariable=startingDayStr, from_=1, to=4, font=(
            "segoe UI", 13), width=10)  # box to set the day we are starting
    startingDaySpinbox.grid(column=2, row=3, ipadx=2, ipady=2, padx=5, pady=5)
    startingDayStr.trace_add('write', lambda nm, idx, mode, whichNum='starDay',
                             startingDayStr=startingDayStr: required_info_entered(whichNum, thingStr=startingDayStr))
    # -----------------------------------------------------------------------------
    # ***********************calendar id entry****************************
    calendarIdLabel = Label(parent, wraplength=150, justify=LEFT)
    calendarIdLabel.grid(column=0, row=4)
    calendarIdClass = calendar_id_entry(parent, calendarIdLabel)
    calendarIdButton = Button(parent, text='calendar id',
                              command=calendarIdClass.menu_to_put_calendar_id, font=("segoe UI", 13))
    calendarIdButton.grid(column=2, row=4)
    #-------------------------------------------------------------------------------
    # *******************creds file button********************************
    credsFileButton = Button(parent,text='select credential file',command=lambda parent = parent: add_creds_file(parent),font=("segoe UI", 13))
    credsFileButton.grid(column=2,row=5, ipadx=2, ipady=2, padx=5, pady=5)
    # -------------------------------------------------------------------------------
    # ***********************continue button******************************
    continueButton = Button(parent, text='continue', font=("segoe UI", 13))
    continueButton.config(command=lambda
                          parent=parent, weekToAddLabel=WeekToAddLabel, amountWeekToAddStr=amountWeekToAddStr,
                          amountWeekToAddSpinbox=amountWeekToAddSpinbox, skipFowrwardLabel=skipFowrwardLabel,
                          amountOfDayToSkipForwardStr=amountOfDayToSkipForwardStr, skipForwardSpinbox=skipForwardSpinbox, startingDayLabel=startingDayLabel,
                          startingDayStr=startingDayStr, startingDaySpinbox=startingDaySpinbox, calendarIdClass=calendarIdClass, calendarIdButton=calendarIdButton,
                          continueButton=continueButton,credsFileButton=credsFileButton:
                          add_to_agenda(
                              parent, weekToAddLabel, amountWeekToAddStr, amountWeekToAddSpinbox, skipFowrwardLabel, amountOfDayToSkipForwardStr,
                              skipForwardSpinbox, startingDayLabel, startingDayStr, startingDaySpinbox, calendarIdClass, calendarIdButton, continueButton, credsFileButton
                          )
                          )
    continueButton.grid(column=4, row=1, ipadx=2, ipady=2, padx=5, pady=5)

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~


class calendar_id_entry():
    """
        purpose: makes the calendar id entry and window and verify if its valid id
    """

    def __init__(self, parent: Tk, calendarIdLabel: Label):
        self.parent = parent
        self.calendarIdLabel = calendarIdLabel
        self.emailOk = False
        self.emailEntryStr = StringVar(self.parent, value='Calendar Id')
        self.emailEntryStrOg = 'Calendar Id'
        self.entryCheck = False
    # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def menu_to_put_calendar_id(self):
        """
        Purpose: to make the window and what needs to be in it
        """
        # *makes the window:
        self.top = Toplevel(self.parent)
        self.top.title('calendar id')
        self.top.focus()
        # ---------------------------------------------------
        # * email entry and verify:
        vcmd = (self.top.register(self.validate), '%P')
        ivcmd = (self.top.register(self.on_invalid),)
        # -----------------------------------
        self.emailEntry = Entry(
            self.top, width=50, textvariable=self.emailEntryStr)
        self.emailEntry.config(validate='focusout',
                               validatecommand=vcmd, invalidcommand=ivcmd)
        self.emailEntry.grid(row=0, column=1, columnspan=2, padx=5)
        self.emailEntryStr.trace_add(
            "write", lambda nm, idx, mode: self.remove_placeholder())
        # ---------------------------------------------------
        # * label if there is an error:
        self.label_error = Label(self.top, foreground='red')
        self.label_error.grid(row=1, column=1, sticky='W', padx=5)
        # ---------------------------------------------------
        # * button to confirm the id:
        self.send_button = Button(
            self.top, text='confirm', command=self.set_calendar_id)
        self.send_button.grid(row=0, column=4, padx=5)
    # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def set_calendar_id(self):
        """
            purpose: set the label with the calendar id if the id entered is valid
        """
        self.top.focus()  # to execute the validation of the entry
        if self.emailOk:
            self.top.destroy()
            required_info_entered('calId')
            self.calendarIdLabel.config(text=self.emailEntryStr.get())
        else:
            showerror("invalid id",
                      "The calendar id is not valid.\nPlease enter a valid id")
    # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def show_error(self, error='', color='black'):
        """
            Purpose: show that the entered id is wrong
        """
        self.label_error['text'] = error
        self.emailEntry['foreground'] = color
    # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def validate(self, value):
        """
            Purpose: Validate the email entry
        """
        pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{3,}\b'
        if re.fullmatch(pattern, value) is False:
            self.emailOk = False
            return False
        self.show_error()
        self.emailOk = True
        return True
    # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def on_invalid(self):
        """
        Show the error message if the data is not valid
        """
        self.show_error('Please enter a valid email', 'red')
    # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def remove_placeholder(self):
        """
            purpose: remove placeholder from the entry
        """
        x = self.emailEntryStr.get()
        if not self.entryCheck:
            for i in range(x.count("", 0)-1):
                try:
                    if self.emailEntryStrOg[i] == x[i]:
                        continue
                    else:
                        y = x[i]
                        self.emailEntryStr.set(y)
                        break
                except:
                    y = x[i]
                    self.emailEntryStr.set(y)
                    break
        self.entryCheck = True
        return self.emailEntryStr

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~


def required_info_entered(whichThing: str = None, thingStr: StringVar = None):
    """
        PURPOSE:to verify that the information needed has been entered
        information that is needed:
                • amount week to add
                • starting day
                • calendar Id
    """
    print("boooo!")
    if whichThing == 'amountWeek':
        if thingStr.get() != "0" and not required_info_entered.amountWeekAddChecked:
            required_info_entered.amountWeekAddChecked = True
        elif thingStr.get() == '0' and required_info_entered.amountWeekAddChecked:
            required_info_entered.amountWeekAddChecked = False
    elif whichThing == 'starDay':
        if thingStr.get() != "0" and not required_info_entered.startDayChecked:
            required_info_entered.startDayChecked = True
        elif thingStr.get() == '0' and required_info_entered.startDayChecked:
            required_info_entered.startDayChecked = False
    elif whichThing == 'calId':
        required_info_entered.calIdEntered = True


required_info_entered.amountWeekAddChecked = False
required_info_entered.startDayChecked = False
required_info_entered.calIdEntered = False

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~


def add_to_agenda(parent: Tk = None,
                  weekToAddLabel: Label = None, amountWeekToAddStr: StringVar = None, amountWeekToAddSpinbox: Spinbox = None, skipFowrwardLabel: Label = None,
                  amountOfDayToSkipForwardStr: StringVar = None, skipForwardSpinbox: Spinbox = None, startingDayLabel: Label = None,
                  startingDayStr: StringVar = None, startingDaySpinbox: Spinbox = None, calendarIdClass: calendar_id_entry = None,
                  calendarIdButton: Button = None, continueButton: Button = None, credsFileButton: Button = None
                  ):
    """
        Purpose: if everything required was entered and adds them to the calendar.
    """
    print('hello potatoos')
    if not required_info_entered.amountWeekAddChecked and not required_info_entered.startDayChecked and not required_info_entered.calIdEntered and not os.path.isfile('credentials.json'):
        if not required_info_entered.amountWeekAddChecked:
            weekToAddLabel.config(fg="red")
        if not required_info_entered.startDayChecked:
            startingDayLabel.config(fg="red")
        if not required_info_entered.calIdEntered:
            calendarIdButton.config(fg="red")
        if not os.path.isfile('credentials.json'):
            credsFileButton.config(fg="red")
        showerror('incomplete information',
                  'there is some required information that has not been entered')
        return
    with open('time.txt', 'r') as f:
        classTimeStartEndList = json.loads(f.readline())
    setup(int(amountOfDayToSkipForwardStr.get()), classTimeStartEndList, int(
        startingDayStr.get()), int(amountWeekToAddStr.get()), calendarIdClass.emailEntryStr.get())

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

def add_creds_file(parent:Tk=None):
    """
        Purpose: to be capable to enter the credential file
    """
    print("hi")
    top = Toplevel(parent)
    top.geometry('700x700')
    chooseFileButton = Button(top,text='select a credential file')
    chooseFileButton.grid(column=2,row=2)
    chosenFileLabelStr = StringVar(top)
    chosenFileLabel = Label(top,textvariable=chosenFileLabelStr)
    chosenFileLabel.grid(column=2,row=3)
    chooseFileButton.config(command=lambda chosenFileLabelStr = chosenFileLabelStr,parent=top:chooseFile(parent,chosenFileLabelStr))

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

def chooseFile(parent:Toplevel,chosenFileLabelStr:StringVar):
    print('hi')
    credsFileDir = filedialog.askopenfilename(title='select credential file',initialdir='/',filetypes=(('JSON Source File', '*.json'),('All File', '*.*')))
    chosenFileLabelStr.set(credsFileDir)
    if os.path.isfile('credentials.json'):
        # Comment: verify if credential file already exist and remove it.
        os.remove('credentials.json')  # import os
    # end if del-file
    with open('credentials.json', 'w') as f:
        # Comment: opens credentials file and puts the credential in it
        with open(f'{credsFileDir}.json', 'r') as fe:
            # Comment: 
            f.write(fe.readline())
        # end readline file
    # end overwrite file
    return chosenFileLabelStr

# ¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦

# ******************************documentation****************************

def documentation_start(parent: Canvas):
    """
    Purpose: haveing documentation
    """
    for i in range(3):
        parent.columnconfigure(i,weight=1)
        parent.rowconfigure(i,weight=1)
    typeOfDocumentationStr = StringVar(parent)
    typeOfDocumentationCombobox = ttk.Combobox(parent,
                textvariable=typeOfDocumentationStr,font=("segoe UI", 13), width=30,state='readonly',
                values=['How to create the cloud project','How to get the credential file','Add your email account as tester','Get a calendar id'])
    typeOfDocumentationCombobox.grid(column=1,row=1)
    
    docGetCredCanvas = Canvas(parent)
    docCreateCloudCanvas = Canvas(parent)
    docAddTestCanvas = Canvas(parent)
    docGetCalIdCanvas = Canvas(parent)
    
    selectButton = Button(parent, text='see this documentation',font=("segoe UI", 13))
    selectButton.grid(column=1,row=2,sticky="N")
    selectButton.focus_set()
    selectButton.config(command= lambda parent=parent,typeOfDocumentationStr=typeOfDocumentationStr, typeOfDocumentationCombobox=typeOfDocumentationCombobox,selectButton=selectButton,docGetCredCanvas=docGetCredCanvas,docCreateCloudCanvas=docCreateCloudCanvas,docAddTestCanvas=docAddTestCanvas,docGetCalIdCanvas=docGetCalIdCanvas:get_documentation(parent,typeOfDocumentationStr,typeOfDocumentationCombobox,selectButton,docGetCredCanvas,docCreateCloudCanvas,docAddTestCanvas,docGetCalIdCanvas))

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

def get_documentation(parent:Canvas=None,typeOfDocumentationStr:StringVar=None,typeOfDocumentationCombobox:ttk.Combobox=None,selectButton:Button=None,docGetCredCanvas:Canvas=None,docCreateCloudCanvas:Canvas=None,docAddTestCanvas:Canvas=None,docGetCalIdCanvas:Canvas=None):
    """
    Purpose: get the selected documentation and show it.
    """
    typeOfDocumentationCombobox.grid_forget()
    typeOfDocumentationCombobox.forget()
    selectButton.grid_forget()
    selectButton.forget()
    typeOfDocumentationStr.trace('w', lambda nm, idx, mode,parent=parent,
                    typeOfDocumentationStr=typeOfDocumentationStr,docGetCredCanvas=docGetCredCanvas,
                    docCreateCloudCanvas=docCreateCloudCanvas,docAddTestCanvas=docAddTestCanvas,docGetCalIdCanvas=docGetCalIdCanvas,
                    typeOfDocumentationComboboxCreateCloud=typeOfDocumentationComboboxCreateCloud,typeOfDocumentationComboboxGetCreds=typeOfDocumentationComboboxGetCreds,
                    typeOfDocumentationComboboxAddTest=typeOfDocumentationComboboxAddTest,typeOfDocumentationComboboxCalId=typeOfDocumentationComboboxCalId:
                    change_doc(parent,typeOfDocumentationStr,
                                docGetCredCanvas,docCreateCloudCanvas,docAddTestCanvas,docGetCalIdCanvas,typeOfDocumentationComboboxCreateCloud,
                                typeOfDocumentationComboboxGetCreds,typeOfDocumentationComboboxAddTest,typeOfDocumentationComboboxCalId)
                )
    #----------------------------------------------------------------
    typeOfDocumentationComboboxCreateCloud = ttk.Combobox(docCreateCloudCanvas,
                textvariable=typeOfDocumentationStr,font=("segoe UI", 13), width=30,state='readonly',
                values=['How to create the cloud project','How to get the credential file','Add your email account as tester','Get a calendar id'])
    typeOfDocumentationComboboxCreateCloud.grid(row=0,column=0)
    #----------------------------------------------------------------
    typeOfDocumentationComboboxGetCreds = ttk.Combobox(docGetCredCanvas,
                textvariable=typeOfDocumentationStr,font=("segoe UI", 13), width=30,state='readonly',
                values=['How to create the cloud project','How to get the credential file','Add your email account as tester','Get a calendar id'])
    typeOfDocumentationComboboxGetCreds.grid(row=0,column=0)
    #----------------------------------------------------------------
    typeOfDocumentationComboboxAddTest = ttk.Combobox(docAddTestCanvas,
                textvariable=typeOfDocumentationStr,font=("segoe UI", 13), width=30,state='readonly',
                values=['How to create the cloud project','How to get the credential file','Add your email account as tester','Get a calendar id'])
    typeOfDocumentationComboboxAddTest.grid(row=0,column=0)
    #----------------------------------------------------------------
    typeOfDocumentationComboboxCalId = ttk.Combobox(docGetCalIdCanvas,
                textvariable=typeOfDocumentationStr,font=("segoe UI", 13), width=30,state='readonly',
                values=['How to create the cloud project','How to get the credential file','Add your email account as tester','Get a calendar id'])
    typeOfDocumentationComboboxCalId.grid(row=0,column=0)
    #---------------------------------------------------------------
    if typeOfDocumentationStr.get() == 'How to create the cloud project':
        typeOfDocumentationComboboxGetCreds.selection_set(0)
        typeOfDocumentationComboboxAddTest.selection_set(0)
        typeOfDocumentationComboboxCalId.selection_set(0)
        docCreateCloudCanvas.selection_set(0)
        docCreateCloudCanvas.pack(expand=1, fill="both")
        doc_create_cloud1(docCreateCloudCanvas)
    #----------------------------------------------------------------
    elif typeOfDocumentationStr.get() == 'How to get credential file':
        typeOfDocumentationComboboxGetCreds.selection_set(1)
        typeOfDocumentationComboboxAddTest.selection_set(1)
        typeOfDocumentationComboboxCalId.selection_set(1)
        docCreateCloudCanvas.selection_set(1)
        docGetCredCanvas.pack(expand=1, fill="both")
        doc_get_creds1(parent,docGetCredCanvas)
    #----------------------------------------------------------------
    elif typeOfDocumentationStr.get() == 'Add your email account as tester':
        typeOfDocumentationComboboxGetCreds.selection_set(2)
        typeOfDocumentationComboboxAddTest.selection_set(2)
        typeOfDocumentationComboboxCalId.selection_set(2)
        docCreateCloudCanvas.selection_set(2)
        docAddTestCanvas.pack(expand=1, fill="both")
        doc_add_tester1(parent,docAddTestCanvas)
    #-------------------------------------------------------------
    elif typeOfDocumentationStr.get() == 'Get a calendar id':
        typeOfDocumentationComboboxGetCreds.selection_set(3)
        typeOfDocumentationComboboxAddTest.selection_set(3)
        typeOfDocumentationComboboxCalId.selection_set(3)
        docCreateCloudCanvas.selection_set(3)
        docGetCalIdCanvas.pack(expand=1, fill="both")
        doc_get_calendar_id1(parent,docGetCalIdCanvas)

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

def change_doc(parent:Canvas=None,typeOfDocumentationStr:StringVar=None,
            docGetCredCanvas:Canvas=None,docCreateCloudCanvas:Canvas=None,docAddTestCanvas:Canvas=None,docGetCalIdCanvas:Canvas=None,
            typeOfDocumentationComboboxCreateCloud:ttk.Combobox=None,typeOfDocumentationComboboxGetCreds:ttk.Combobox=None,
            typeOfDocumentationComboboxAddTest:ttk.Combobox=None,typeOfDocumentationComboboxCalId:ttk.Combobox=None):
    """
    Purpose: to change the documentation
    """
    if docGetCredCanvas.pack_slaves() != []:selected = 'getcreds'
    elif docCreateCloudCanvas.pack_slaves() != []: selected = 'createcloud'
    elif docAddTestCanvas.pack_slaves() != []: selected = 'addtest'
    elif docGetCalIdCanvas.pack_slaves()!= []: selected = 'getcalid'
    if typeOfDocumentationStr.get() == 'How to get the credential file' and selected != 'getcreds':
        if selected == 'createcloud': docCreateCloudCanvas.pack_forget()
        if selected == 'addtest': docAddTestCanvas.pack_forget()
        if selected == 'getcalid': docGetCalIdCanvas.pack_forget()
        typeOfDocumentationComboboxGetCreds.selection_set(0)
        typeOfDocumentationComboboxAddTest.selection_set(0)
        typeOfDocumentationComboboxCalId.selection_set(0)
        docCreateCloudCanvas.selection_set(0)
        docGetCredCanvas.pack(expand=1,fill="both")


#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

def doc_create_cloud1(parent:Canvas):
    """
    Purpose: makes the first page of the create cloud documentation
    """
    

#¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦

if __name__ == '__main__':
    fenetre = Tk()
    fenetre.geometry('700x700')
    numDaysStr = StringVar()
    numClassStr = StringVar()
    classNameStr = StringVar()
    class_time_start_end.classTimeStartEndList = {}
    setup_main(fenetre)
    fenetre.mainloop()
