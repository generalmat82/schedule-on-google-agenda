from tkinter import *
from tkinter import ttk
# *for making the actual schedule with class name and ect
class NotificationChoiceClass():
    def __init__(self,parent,notifList):
        self.notifSettings = Toplevel(parent)
        self.notifSettings.geometry("750x250")
        self.notifSettings.title("boo")
        self.notifSettings.focus()
        self.layout_notif(parent,notifList)
    # -------------------------------------------------------------------------------------------------------------------------------

    def layout_notif(self,parent,notifList):
        self.typeNotifStr = StringVar(self.notifSettings, value='popup')
        self.typeNotif = ttk.Combobox(self.notifSettings, values=[
            'email', 'popup'], textvariable=self.typeNotifStr, state='readonly')  # *for saying what type it is
        self.typeNotif.grid(column=1, row=2)
        # -------------------------------------------------------------------------------------------------------------------------------
        self.minTime = 0
        self.maxTime = 40320
        self.timeBeforeStr = StringVar(self.notifSettings, value=5)  # type: ignore
        self.timeBefore = Spinbox(self.notifSettings, from_=self.minTime, to=self.maxTime,
            wrap=True, textvariable=self.timeBeforeStr
        )  # amount of time before event
        self.timeBefore.grid(column=2, row=2)
        # -------------------------------------------------------------------------------------------------------------------------------
        self.typeOfTimeStr = StringVar(self.notifSettings, value='minutes')
        self.typeOfTime = ttk.Combobox(self.notifSettings, values=[
            'minutes', 'hours', 'days', 'weeks'], textvariable=self.typeOfTimeStr, state='readonly'
        )
        self.typeOfTime.grid(column=3, row=2)
        self.typeOfTimeStr.trace_add('write', lambda nm, idx, mode, x=self.typeOfTimeStr: self.check_time_type(x))
        # -------------------------------------------------------------------------------------------------------------------------------
        self.confirmButton = Button(self.notifSettings, text='confirm settings', command=lambda parent=parent, notifList=notifList: self.notif_settings_taking(parent,notifList))
        self.confirmButton.grid(column=4, row=2)

    def check_time_type(self, x):
        x = x.get()
        if x == 'minutes':
            self.timeBefore.config(to=40320)
        elif x == 'hours':
            self.timeBefore.config(to=672)
        elif x == 'days':
            self.timeBefore.config(to=28)
        elif x == 'weeks':
            self.timeBefore.config(to=4)
    # -------------------------------------------------------------------------------------------------------------------------------

    def notif_settings_taking(self,parent,notifList):
        time = int(self.timeBefore.get())
        if self.typeOfTime.get() == 'hours':
            time = time*60
        elif self.typeOfTime.get() == 'days':
            time = (time*24)*60
        elif self.typeOfTime.get() == 'weeks':
            time = ((time*7)*24)*60
        self.notifListReminder = {
            "method": self.typeNotifStr.get(),
            'minutes': time
        }
        self.text = f'notification by {self.typeNotifStr.get()}, {self.timeBefore.get()} {self.typeOfTime.get()} before the event'
        add_notif_to_notif_screen(parent,notifList)
        self.notifSettings.destroy()


def notif_screen(parent,notifList):
    notifScreenOp = Toplevel(parent)
    notifScreenOp.geometry("750x250")
    notifScreenOp.focus()
    addNotifButton = Button(notifScreenOp,text='Add a notification',command=lambda NotifScreenOp=notifScreenOp,notifList=notifList: add_notif(NotifScreenOp,notifList))
    addNotifButton.grid(row=0, column=0)
    doneButton = Button(notifScreenOp,text='Finish',command=lambda NotifScreenOp=notifScreenOp: done_notif(NotifScreenOp))
    doneButton.grid(row=1,column=0)

def add_notif(parent,notifList):
    add_notif.notificatList.append(NotificationChoiceClass(parent,notifList))

def add_notif_to_notif_screen(parent,notifList):
    text = add_notif.notificatList[-1].text
    Label(parent,text=text).grid(column=2,row=len(add_notif.notificatList)-1)
    notifList.append(add_notif.notificatList[-1].notifListReminder)
    return notifList

add_notif.notificatList = []

def done_notif(notifScreenOp):
    notifScreenOp.destroy()