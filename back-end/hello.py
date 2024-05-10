from flask import Flask, request, redirect, url_for
from werkzeug.utils import secure_filename
import os

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = '/uploads'

@app.route("/")
def hello_world():
    return "Hello, World!"

@app.route('/uploader', methods=['POST'])
def upload_file():
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
