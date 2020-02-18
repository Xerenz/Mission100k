import csv
import json
import pandas as pd 
import schedule
import time
import firebase_admin
from firebase_admin import credentials, firestore


cred = credentials.Certificate('./../ServiceAccountKey.json')
default_app = firebase_admin.initialize_app(cred)
db = firestore.client()

# no. of documents already parsed
global doc_count
doc_count = 0
# time_ = time.time()
def parse():
    global doc_count
    data = open('./../mission_flight/raw_data.txt', encoding='utf-8', errors='ignore')
    def is_number(s):
        try:
            float(s)
            return True
        except ValueError:
            return False

    content = data.readlines()
    # print(len(content))
    coordinates = []
    index_line = 0
    for each_line in content:
        try:
            _, link, _ = each_line.split("'")

            _, location = link.split("=")
            _, coords = location.split(":")
            lat_, long_ = coords.split(",")
            
            if is_number(lat_) and is_number(long_):
                lat_ = float(lat_)
                long_ = float(long_)
                # checking for valid coordinates
                if (lat_ >= -90 and lat_ <= 90) and (long_ >= -180 and long_ <= 180):
                    if (lat_ >= 11 and lat_ <= 12) and (long_ >= 75 and long_ <= 77):
                        if [lat_, long_] not in coordinates[-1:]:
                            coordinates.append([lat_, long_])
                            index_line += 1
        except:
            pass
    parse_coordinates = []
    
    for index, coord in enumerate(coordinates[:-1]):
        if (abs(coord[0] - coordinates[index + 1][0]) <= 0.004 and (abs(coord[1] - coordinates[index + 1][1]) <= 0.004)):
            parse_coordinates.append(coord)

    coord_dict = {}
    coord_list = []
    for coord in parse_coordinates:
        coord_dict["LAT"] = coord[0]
        coord_dict["LONG"] = coord[1]
        coord_list.append(coord_dict)
    

    
    doc_ref = db.collection(u'main_coordinates')
    for index, element in enumerate(coord_list):
        # add if already exists check
        if index >= doc_count:
            element["index"] = index
            doc = doc_ref.document(str(index))
            doc.set(element)
            doc_count += 1
    print('.', end='')

parse()
now = time.time()
# print(now - time_)
# schedule.every(5).seconds.do(parse)



# while True:

#     schedule.run_pending()
#     time.sleep(1)
    


