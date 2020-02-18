import csv
import json
import pandas as pd 
import schedule
import time
import firebase_admin
from firebase_admin import credentials, firestore


cred = credentials.Certificate('./ServiceAccountKey.json')
default_app = firebase_admin.initialize_app(cred)
db = firestore.client()

def parse():
    data = open('mission_flight/raw_data.txt', encoding='utf-8', errors='ignore')
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
    print(len(parse_coordinates))
    
    
    # improvements to be added
    with open('main_coordinates.csv', mode='w') as coords_file:
        coord_writer = csv.writer(coords_file)
        coord_writer.writerow(['LAT', 'LONG'])
        for coord in parse_coordinates:
            coord_writer.writerow([coord[0], coord[1]])
            
    # converting the files to csv
    csv_file = pd.DataFrame(pd.read_csv('main_coordinates.csv'))
    csv_file.to_json('main_coords.json', orient='records', indent=4)

parse()

doc_ref = db.collection(u'main_coordinates')
with open('main_coords.json') as f:
    data = json.load(f)

for index, element in enumerate(data):
    # add if already exists check
    element["index"] = index
    doc_ref.add(element)
    
schedule.every(5).seconds.do(parse)


while True:

    schedule.run_pending()
    time.sleep(1)
    


    
    