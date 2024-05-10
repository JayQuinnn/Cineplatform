from flask import Flask, request, redirect, url_for
from werkzeug.utils import secure_filename
import os
from flask_cors import CORS
app = Flask(__name__)
# flask --app hello run -p 8000
CORS(app)  # Enable CORS for all routes
app.config['UPLOAD_FOLDER'] = '/Users/jochem/Documents/GitHub/Cineplatform/Cineplatform/back-end/uploads/'

@app.route("/")
def hello_world():
    return "Hello, World!"

@app.route('/uploader', methods=['POST'])
def upload_file():
    print('-------------------')
    print(request.files)
    print('-------------------')
    if 'videoFile' not in request.files:
        return 'No file part'
    videoFile = request.files['videoFile']
    if videoFile.filename == '':
        return 'No selected file'
    if videoFile:
        filename = secure_filename(videoFile.filename)
        videoFile.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        return f'File {filename} uploaded successfully'
    return 'File upload failed'

# if __name__ == '__main__':
#     app.run(debug=True)
