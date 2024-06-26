# flask --app cineplatformAPI run -p 8000
import json
import uuid
import yagmail
from flask import Flask, request, redirect, url_for, jsonify, make_response, send_file
from werkzeug.utils import secure_filename
import os
from flask_cors import CORS
import DaVinciResolveScript as dvr_script
from filehashing import addHashLink, decodeHashLink, clearHashStorage, showAllHashedFiles
from db import addEntry, updateEntry, getAllEntries, clearDB, getEntry
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
app.config['OUTPUT_FOLDER'] = '/Users/jochem/Documents/GitHub/Cineplatform/Cineplatform/back-end/uploads/output/'

@app.route("/")
def hello_world():
    return "Hello, World!"

@app.route("/download/<uuid>")
def downloadFile(uuid):
    entry = getEntry(uuid)
    # add check that file is done rendering
    # mark file as downloaded
    downloadPath = app.config['OUTPUT_FOLDER'] + entry['outputName']
    return send_file(downloadPath, as_attachment=True)

@app.route('/clearhashstorage')
def clearingstorage():
    clearDB()
    return 'hash storage cleared.'

@app.route('/allfiles')
def showAllFiles():
    allFiles = getAllEntries()
    return make_response(jsonify(allFiles), 200)

@app.route('/renderstatus')
def getRenderStatus():
    project = projectManager.GetCurrentProject()
    renderStatus = project.IsRenderingInProgress()
    return make_response(jsonify({'Render status': str(renderStatus)}), 200)

@app.route('/renderlist')
def getRenderList():
    project = projectManager.GetCurrentProject()
    renderList = project.GetRenderJobList()
    return make_response(jsonify({'Render Queue': renderList}), 200)

@app.route('/getproperty')
def remoteClipPropertyGrabber():
    project = projectManager.GetCurrentProject()
    projectSettings = project.GetSetting()
    mediaPool = project.GetMediaPool()
    currentTimeline = mediaPool.GetCurrentFolder().GetClipList()[0].GetClipProperty()
    return mediaPool.GetCurrentFolder().GetClipList()[0].GetClipProperty()

@app.route('/projectsettings')
def remoteProjectSettingsGrabber():
    project = projectManager.GetCurrentProject()
    projectSettings = project.GetSetting()
    return projectSettings

@app.route('/uploader/<email>', methods=['POST'])
def upload_file(email):
    #TODO: Check extension of base file and change output extension to the same one.
    if 'videoFile' not in request.files:
        return 'No file part'
    videoFile = request.files['videoFile']
    settings = json.loads(request.form['Settings'])
    if videoFile.filename == '':
        return 'No selected file'
    if videoFile:
        filename = secure_filename(videoFile.filename)
        videoFile.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        pathFileName = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        fileuuid = str(uuid.uuid4())
        extension = pathFileName.split(".")[-1]
        newfileName = fileuuid+'.'+extension
        newPathName = os.path.join(app.config['UPLOAD_FOLDER'], newfileName)
        os.rename(pathFileName, newPathName)
        outputName = fileuuid+'_output.mov'
        addEntry(fileuuid, filename,outputName,email)
        emailHandler(email=email, UUIDcode=fileuuid)
        sendToResolve(pathFileName=newPathName, fileName=newfileName ,outputName=fileuuid+'_output', parsedSettings=settings)
        return make_response(jsonify({'UUID': f'{fileuuid}'}), 200)
    return 'File upload failed'

def sendToResolve(pathFileName, fileName, outputName, parsedSettings):
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
    clipFPS = clip[0].GetClipProperty('FPS')
    setHeight = None
    setWidth = None
    if parsedSettings['Resolution'] == 'Auto':
        clipResolution = clip[0].GetClipProperty('Resolution')
        before_x, after_x = clipResolution.split('x')
        sourceWidth = int(before_x)
        sourceHeight = int(after_x)
        setHeight = sourceHeight
        setWidth = sourceWidth
    elif parsedSettings['Resolution'] == 'HD':
        setHeight = '1080'
        setWidth = "1920"
    elif parsedSettings['Resolution'] == 'QHD':
        setHeight = '1440'
        setWidth = "2560"
    elif parsedSettings['Resolution'] == 'UHD':
        setHeight = '2160'
        setWidth = "3480"
    #Hotfix 1 - Resolution
    project.SetSetting('timelineResolutionWidth', str(setWidth))
    project.SetSetting('timelineResolutionHeight', str(setHeight))
    project.SetSetting('timelineFrameRate', str(clipFPS))
    timeline = mediaPool.CreateTimelineFromClips('timeline',clip)
    # project.SetSetting('superScale', 2, 1, 0.5)
    # clip[0].SetClipProperty('Super Scale', 2, 1, 0.5)
    #Hotfix 2 - Force Resolution settings
    timeline.SetSetting('timelineOutputResolutionHeight', str(setHeight))
    timeline.SetSetting('timelineOutputResolutionWidth',str(setWidth))
    timeline.SetSetting('timelineResolutionHeight',str(setHeight))
    timeline.SetSetting('timelineResolutionWidth',str(setWidth))
    # Set the render settings
    Settings = {
        'SelectAllFrames': True,
        "TargetDir": "/Users/jochem/Documents/GitHub/Cineplatform/Cineplatform/back-end/uploads/output/",
        "CustomName": f"{outputName}",
        "VideoQuality": 0,
        "ExportVideo": True,
        "ExportAudio": True,
        "FrameRate": str(clipFPS),
    }
    print(Settings)
    project.SetRenderSettings(Settings)
    print('Added project ' + pname + ' to render queue.' )
    # Render the timeline
    render_job = project.AddRenderJob()
    project.StartRendering()

def emailHandler(email, UUIDcode):
    if email != 'none':
        send_email(recipient_email=email, UUIDcode=UUIDcode)
    return

def send_email(recipient_email, UUIDcode):
    # Your email credentials
    sender_email = "videnhancenotifications@gmail.com"
    # Email subject and content
    subject = "vidEnhance - The code to your enhanced video!"
    body = f"Hi! Your video is almost done rendering! Here is the code: {UUIDcode}."

    try:
        # Initialize yagmail SMTP connection
        yag = yagmail.SMTP(sender_email, oauth2_file="./google_creds.json")

        # Send the email
        yag.send(
            to=recipient_email,
            subject=subject,
            contents=body
        )
        print("Email sent successfully!")
    except Exception as e:
        print(f"Error sending email: {e}")


if __name__ == '__main__':
   app.run(debug=True, port=5501, host='10.2.89.108')
