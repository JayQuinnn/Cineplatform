import json
template = {
    "18052024220122Expor.mov": {
        "originalName" : "Export.mov",
        "outputName" : "Export_18052024220122_Output.mov",
        "finishedRendering" : True,
        "progress" : 100,
        "email" : "Lasseisalovelyman@skynet.net",
        "downloaded": False
    }
}
#Make async, then handle a lock var. Every function should check var before writing.
def addEntry(key,ogName, outputName, email):
    data = {
        "originalName" : f"{ogName}",
        "outputName" : f"{outputName}",
        "finishedRendering" : False,
        "progress" : 0,
        "email" : f"{email}",
        "downloaded": False
    }
    with open("/Users/jochem/Documents/GitHub/Cineplatform/Cineplatform/back-end/currentfiles.json", "r") as file:
        existing_data = json.load(file)
    existing_data[key] = data
    with open("/Users/jochem/Documents/GitHub/Cineplatform/Cineplatform/back-end/currentfiles.json", "w") as file:
       json.dump(existing_data, file, indent=4)
    return

def updateEntry(key, finishedRendering=None, progress=None, downloaded=None):
    with open("/Users/jochem/Documents/GitHub/Cineplatform/Cineplatform/back-end/currentfiles.json", "r") as file:
        existing_data = json.load(file)
    if finishedRendering is not None:
        existing_data[key]["finishedRendering"] = finishedRendering
    if progress is not None:
        existing_data[key]["progress"] = progress
    if downloaded is not None:
        existing_data[key]["downloaded"] = downloaded
    with open("/Users/jochem/Documents/GitHub/Cineplatform/Cineplatform/back-end/currentfiles.json", "w") as file:
        json.dump(existing_data, file, indent=4)
    return

def getEntry(key):
    with open("/Users/jochem/Documents/GitHub/Cineplatform/Cineplatform/back-end/currentfiles.json", "r") as file:
        existing_data = json.load(file)
    return existing_data[key]

def getAllEntries():
    with open("/Users/jochem/Documents/GitHub/Cineplatform/Cineplatform/back-end/currentfiles.json", "r") as file:
        existing_data = json.load(file)
    return existing_data

def clearDB():
    with open("/Users/jochem/Documents/GitHub/Cineplatform/Cineplatform/back-end/currentfiles.json", "w") as file:
        file.truncate()
        file.write("{}")
    return


# addEntry('18052024220122hello.mp4', 'hello.mp4', 'hello_18052024220122_output.mp4', 'Lasseisaniceguy@skynet.net')
# updateEntry('18052024220122hello.mp4', True, 69)
# updateEntry('18052024220122hello.mp4', downloaded=True)
# print(str(getAllEntries()))
# print(str(getEntry('18052024220122hello.mp4')))
# clearDB()
# print(str(getAllEntries()))