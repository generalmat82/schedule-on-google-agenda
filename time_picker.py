from tkinter import *


class TimeSelection():
    def __init__(self, parent):
        """
            Purpose: Construct the base of the selection gui without showing it.
        """
        self.maxh=5
        self.minh=0
        self.format12h='24h'
            #-------------------------------------------------------------------------------------------------------------------------------
        self.selectedAmPmStr = StringVar(value='am')
        self.amButton = Radiobutton(parent,text='AM',value='am',variable=self.selectedAmPmStr)
        self.pmButton = Radiobutton(parent,text='PM',value='pm',variable=self.selectedAmPmStr)
        #-------------------------------------------------------------------------------------------------------------------------------
        self.hourSelectedStr=StringVar(parent,'5')
        self.hourSpinbox = Spinbox(parent,from_=self.minh,to=self.maxh,wrap=True,textvariable=self.hourSelectedStr,width=5,state="readonly")
        #-------------------------------------------------------------------------------------------------------------------------------
        self.minSelectedStr=StringVar(parent,'30')
        self.minSpinbox = Spinbox(parent,from_=0,to=59,wrap=True,textvariable=self.minSelectedStr,width=5)    # ,state="readonly"
        #-------------------------------------------------------------------------------------------------------------------------------
        self.secSelectedStr=StringVar(parent,'00')
        self.secSpinbox = Spinbox(parent,from_=0,to=59,wrap=True,textvariable=self.secSelectedStr,width=5) 
        #-------------------------------------------------------------------------------------------------------------------------------
        self.lastValueSec = ""
        self.lastValueMin = ""        
        self.minSelectedStr.trace("w",self.trace_var_hours)
        self.secSelectedStr.trace("w",self.trace_varsec)
    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    def place_stuff(self, parent,timeFormat12hOr24h='24h'):
        """
            Purpose: place the gui on the screen on top
        """
        self.hourSpinbox.grid(row=0,column=0)
        self.minSpinbox.grid(row=0,column=1)
        self.secSpinbox.grid(row=0,column=2)
        #---------------------------------------------------------------------------------------------------------------------------
        if timeFormat12hOr24h == '12h':
            #if the time format is 12 hour it will add the radio buttons
            self.amButton.grid(column=3,row=0)
            self.pmButton.grid(column=3,row=1)
            self.format12h = '12h'
        #----------------------------------------------------------------
        if self.format12h == '12h' and timeFormat12hOr24h == '24h' :
            #if we go to 24 hour format and we used to be in 12 hour to remove radio button
            self.amButton.grid_forget()
            self.pmButton.grid_forget()
            self.format12h = '24h'
        parent.update()
    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    def trace_var_hours(self,*args):
        """
            Purpose: trace the minutes spinbox so if it goes back to 0 it will add a hour
        """
        if self.lastValueMin == "59" and self.minSelectedStr.get() == "0":
            self.hourSelectedStr.set(str(int(self.hourSelectedStr.get())+1 if self.hourSelectedStr.get() !="23" else 0))
        self.lastValueMin = self.minSelectedStr.get()
    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    def trace_varsec(self,*args):
        """
            Purpose: trace the second spinbox so if it goes back to 0 it will add a minute
        """
        if self.lastValueSec == "59" and self.secSelectedStr.get() == "0":
            self.minSelectedStr.set(str(int(self.minSelectedStr.get())+1 if self.minSelectedStr.get() !="59" else 0))#adds a min to munute spinbox if its not at 59 if it is it dosent modifi
            if self.lastValueMin == "59":
                self.hourSelectedStr.set(str(int(self.hourSelectedStr.get())+1 if self.hourSelectedStr.get() !="23" else 0))
        self.lastValueSec = self.secSelectedStr.get()
    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    def make_time(self,):
        """
            Purpose: make the time string and returns it
        """
        if self.format12h == "12h" and self.selectedAmPmStr.get() == 'pm' and self.hourSelectedStr.get() != "12": hour = str(int(self.hourSelectedStr.get())+12).zfill(2)
        else: hour = self.hourSelectedStr.get().zfill(2)
        self.time_complete = f"{hour}:{self.minSelectedStr.get().zfill(2)}:{self.secSelectedStr.get().zfill(2)}"
        return self.time_complete


#===============================================================================================================================

def selected_format_12h(parent,time_select,doneButton):
    """
    Purpose: adds the gui if the selected format is 12h
    """
    time_select.maxh = 12
    time_select.minh = 1
    time_select.hourSpinbox.config(from_=1)
    time_select.hourSpinbox.config(to=12)
    time_select.place_stuff(parent,'12h')
    doneButton.grid(column=4,row=5)
    return time_select
#-------------------------------------------------------------------------------------------------------------------------------
def selected_format_24h(parent,time_select,doneButton):
    """
    Purpose: adds the gui if the selected format is 24h
    """
    time_select.maxh = 23
    time_select.minh = 0
    time_select.hourSpinbox.config(from_=0)
    time_select.hourSpinbox.config(to=23)
    time_select.place_stuff(parent)
    doneButton.grid(column=4,row=5)
    return time_select
#-------------------------------------------------------------------------------------------------------------------------------
def setup(parent,doneButton):
    """
        Purpose: setup to make the time selction
    """
    timeSelect = TimeSelection(parent)
    button12h = Button(parent,text='12 hours form',command=lambda parent=parent,x=timeSelect:selected_format_12h(parent,x,doneButton))
    button12h.grid(column=3,row=2)
    button24h = Button(parent,text='24 hours form',command=lambda parent=parent,x=timeSelect:selected_format_24h(parent,x,doneButton))
    button24h.grid(column=3,row=3)
    return timeSelect
#===============================================================================================================================


