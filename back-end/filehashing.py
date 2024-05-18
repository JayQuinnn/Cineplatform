import sys
import time
from datetime import date

def generateHash(filename):
    today = date.today()
    formatted_date = today.strftime("%d%m%Y")  # dd/mm/YYYY format
    t = time.localtime()
    current_time = time.strftime("%H%M%S", t)
    convertedfilename = formatted_date + current_time + filename[:5] + filename[-4:]
    print(convertedfilename)
    return convertedfilename

filename = generateHash('exportius-5551890843jiffjkdlmfeaiuj.mp4')



