# TODO:
#     - FIX RESOLUTION
#     - FIX ENCODING -> mp4

#!/usr/bin/env python
import DaVinciResolveScript as dvr_script
import sys
# 1. Assign Resolve
resolve = dvr_script.scriptapp("Resolve")
# 2. Get a Project Manager
projectManager = resolve.GetProjectManager ()
# 3. Setup a Project
pname = input('Insert the name for this project ')
project = projectManager.CreateProject (pname)

print(project.GetSetting('timelineResolutionWidth'))
print(project.GetSetting('timelineResolutionHeight'))
# 4. Object of MediaPool is gotten from project.
mediaPool = project.GetMediaPool()
# 5. Media Storage
mediaStorage = resolve. GetMediaStorage()
# 5.1. Import Media
clip = mediaPool. ImportMedia( ['/Users/jochem/Desktop/IMG_0612.MOV'])
print('CLIPRESOLUTION:')
print(clip[0].GetClipProperty('Resolution'))
clipResolution = clip[0].GetClipProperty('Resolution')


before_x, after_x = clipResolution.split('x')
sourceWidth = int(before_x)
print('Source Width: ' + str(sourceWidth))
sourceHeight = int(after_x)
print('Source Height: ' + str(sourceHeight))


project.SetSetting('timelineResolutionWidth', str(sourceWidth))
project.SetSetting('timelineResolutionHeight', str(sourceHeight))


# 7. Create an empty timeline
# tl = mediaPool. CreateEmptyTimeline('t1')
# # 8. Try to get a current timeline
# timeline = project.GetCurrentTimeline()
# # if not, then try to get the first timeline and set it to current
# if not timeline:
#     if project. GetTimelineCount() > 0:
#         timeline = project.GetTimelineByIndex(1)
#         project. SetCurrentTimeline(timeline)
# # 9. Append Clips to the timeline
# appended = mediaPool.AppendToTimeline(clip)

timeline = mediaPool.CreateTimelineFromClips('timeline',clip)

print(timeline.GetSetting())
timeline.SetSetting('timelineOutputResolutionHeight', str(sourceHeight))
timeline.SetSetting('timelineOutputResolutionWidth',str(sourceWidth))
timeline.SetSetting('timelineResolutionHeight',str(sourceHeight))
timeline.SetSetting('timelineResolutionWidth',str(sourceWidth))
print("-------------")
print(timeline.GetSetting())
# Set the render settings
Settings = {
    'SelectAllFrames': True,
    "TargetDir": "/Users/jochem/Documents/GitHub/Cineplatform/Cineplatform/back-end/uploads/output/",
    "CustomName": "output",
    "VideoQuality": 0,
    "ExportVideo": True,
    "ExportAudio": True,
    # "FormatWidth": videoWidth,
    # "FormatHeight": videoHeight,
}
project.SetRenderSettings(Settings)

# Render the timeline

render_job = project.AddRenderJob()
# project.StartRendering()



