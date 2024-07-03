from flask import Flask, request, redirect, url_for
import os

r_server = Flask(__name__)
UPLOAD_FOLDER = '/home/kali/Desktop/CapturedData'
r_server.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@r_server.route('/')
def server_test():
    return 'Welcome to the Triskelion remote server'

@r_server.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return 'No file part', 400
    file = request.files['file']
    if file.filename == '':
        return 'No selected file', 400
    if file:
        filename = file.filename
        file.save(os.path.join(r_server.config['UPLOAD_FOLDER'], filename))
        return 'File uploaded successfully', 200

if __name__ == '__main__':
    if not os.path.exists(UPLOAD_FOLDER):
        os.makedirs(UPLOAD_FOLDER)
    r_server.run(host='0.0.0.0', port=5000)
