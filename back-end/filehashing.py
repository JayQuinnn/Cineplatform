import sys
import time
from datetime import date
import json

def generateHash(filename):
    today = date.today()
    formatted_date = today.strftime("%d%m%Y")  # dd/mm/YYYY format
    t = time.localtime()
    current_time = time.strftime("%H%M%S", t)
    convertedfilename = formatted_date + current_time + filename[:5] + filename[-4:]
    print(convertedfilename)
    return convertedfilename

def addHashLink(originalFilename):
    hashedFilename = generateHash(originalFilename)
    with open("/Users/jochem/Documents/GitHub/Cineplatform/Cineplatform/back-end/currentfiles.json", "r") as file:
        existing_data = json.load(file)
    existing_data[hashedFilename] = originalFilename
    with open("/Users/jochem/Documents/GitHub/Cineplatform/Cineplatform/back-end/currentfiles.json", "w") as file:
       json.dump(existing_data, file, indent=4)
    print("New key-value pair added successfully!")
    return hashedFilename

def decodeHashLink(hashedFilename):
    with open('/Users/jochem/Documents/GitHub/Cineplatform/Cineplatform/back-end/currentfiles.json', 'r') as json_file:
        data = json.load(json_file)
    value = data.get(hashedFilename)
    if value:
        print(f"Value for key '{hashedFilename}': {value}")
        return value
    else:
        print(f"Key '{hashedFilename}' not found in the JSON data.")
        return "Key '{hashedFilename}' not found in the JSON data."


def clearHashStorage():
    with open("/Users/jochem/Documents/GitHub/Cineplatform/Cineplatform/back-end/currentfiles.json", "w") as file:
        file.truncate()
        file.write("{}")
    return


