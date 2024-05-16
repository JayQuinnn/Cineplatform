import DaVinciResolveScript as dvr_script
import sys
# 1. Assign Resolve
resolve = dvr_script.scriptapp("Resolve")
# 2. Get a Project Manager
projectManager = resolve.GetProjectManager ()
# 3. Setup a Project
pname = input('Insert the name for this project ')
project = projectManager.CreateProject (pname)
# 4. Object of MediaPool is gotten from project.
mediaPool = project.GetMediaPool()
# 5. Media Storage
mediaStorage = resolve.GetMediaStorage()
# 5.1. Import Media
clip = mediaPool.ImportMedia( ['/Users/jochem/Documents/GitHub/Cineplatform/Cineplatform/back-end/uploads/JochemCrab_InteractiveMotion_Les1.mov'])
clipResolution = clip[0].GetClipProperty('Resolution')
#Set timeline to clip resolution
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
# Render the timeline
render_job = project.AddRenderJob()
# project.StartRendering()


