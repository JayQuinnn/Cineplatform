# flask --app cineplatformAPI run -p 8000
from flask import Flask, request, redirect, url_for
from werkzeug.utils import secure_filename
import os
from flask_cors import CORS
import DaVinciResolveScript as dvr_script
print('Davinci Resolve imported sucessfully.')
import sys
# 1. Assign Resolve
resolve = dvr_script.scriptapp("Resolve")
# 2. Get a Project Manager
projectManager = resolve.GetProjectManager ()
print('Davinci Resolve hook complete')
app = Flask(__name__)
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
        pathFileName = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        sendToResolve(pathFileName=pathFileName, fileName=filename)
        return f'File {filename} uploaded successfully'
    return 'File upload failed'

def sendToResolve(pathFileName, fileName):
    print('Sending ' + str(pathFileName) + ' to resolve.')
    # 3. Setup a Project
    pname = fileName
    project = projectManager.CreateProject (pname)
    print('Project made called: ' + pname)
    # 4. Object of MediaPool is gotten from project.
    mediaPool = project.GetMediaPool()
    # 5. Media Storage
    mediaStorage = resolve.GetMediaStorage()
    # 5.1. Import Media
    clip = mediaPool.ImportMedia( [pathFileName])
    print('Imported file: ' + pname)
    clipResolution = clip[0].GetClipProperty('Resolution')
    before_x, after_x = clipResolution.split('x')
    sourceWidth = int(before_x)
    sourceHeight = int(after_x)
    #Hotfix 1 - Resolution
    project.SetSetting('timelineResolutionWidth', str(sourceWidth))
    project.SetSetting('timelineResolutionHeight', str(sourceHeight))
    timeline = mediaPool.CreateTimelineFromClips('timeline',clip)
    #Hotfix 2 - Force Resolution settings
    timeline.SetSetting('timelineOutputResolutionHeight', str(sourceHeight))
    timeline.SetSetting('timelineOutputResolutionWidth',str(sourceWidth))
    timeline.SetSetting('timelineResolutionHeight',str(sourceHeight))
    timeline.SetSetting('timelineResolutionWidth',str(sourceWidth))
    # Set the render settings
    Settings = {
        'SelectAllFrames': True,
        "TargetDir": "/Users/jochem/Documents/GitHub/Cineplatform/Cineplatform/back-end/uploads/output/",
        "CustomName": "output",
        "VideoQuality": 0,
        "ExportVideo": True,
        "ExportAudio": True,
    }
    project.SetRenderSettings(Settings)
    print('Added project ' + pname + ' to render queue.' )
    # Render the timeline
    render_job = project.AddRenderJob()
    # project.StartRendering()

if __name__ == '__main__':
   app.run(debug=True, port=8000)
