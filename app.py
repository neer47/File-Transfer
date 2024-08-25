from flask import Flask, request, redirect, render_template
import requests
import os

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # Limit file size to 16 MB

# Ensure upload folder exists
if not os.path.exists(app.config['UPLOAD_FOLDER']):
    os.makedirs(app.config['UPLOAD_FOLDER'])

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return redirect(request.url)
    file = request.files['file']
    if file.filename == '':
        return redirect(request.url)
    if file:
        # Send file to the server
        server_url = 'http://localhost:5001/upload'  # URL of your server
        files = {'file': (file.filename, file, file.mimetype)}
        response = requests.post(server_url, files=files)
        if response.status_code == 200:
            return 'File uploaded successfully to the server'
        else:
            return 'File upload failed on the server'
    return 'File upload failed'

if __name__ == '__main__':
    app.run(debug=True)
