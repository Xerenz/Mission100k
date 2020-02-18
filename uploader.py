# the firebase uploader plugin
# to upload the raw data constantly
# to be run constantly using scheduler
import firebase_admin
from firebase_admin import credentials, firestore
import schedule
import time

cred = credentials.Certificate('./ServiceAccountKey.json')
default_app = firebase_admin.initialize_app(cred)
db = firestore.client()
print("uploading ", end='')
def upload_data():
    data = open('./mission_flight/new_data.txt', encoding='utf-8', errors='ignore')
    content = data.read()
    print('.', end='')
    doc_ref = db.collection(u'raw-data').document(u'data')
    doc_ref.set({u'new_data': content})

schedule.every(4).seconds.do(upload_data)

while True:
    schedule.run_pending()
    time.sleep(1)


