import RPi.GPIO as GPIO
import time
import serial
from pyrebase import pyrebase

from buzzerSensorManager import BuzzerSensorManager
from proximitySensorManager import ProximitySensorManager
from cameraSensorManager import CameraSensorManager
from imageUploadManager import ImageUploadManager
from hmiDisplayManager import HmiDisplayManager
from enums import HmiDisplayPageEnum

proximitySensor = ProximitySensorManager()
ubb = BuzzerSensorManager()
cam = CameraSensorManager()
imu = ImageUploadManager()
hmi = HmiDisplayManager()

config = {
  "apiKey": "AIzaSyDdW0WLhoJZyqNIOh5ha-CkrD1cEBIIMso",
  "authDomain": "peepnee-backend.firebaseapp.com",
  "databaseURL": "https://peepnee-backend.firebaseio.com",
  "storageBucket": "peepnee-backend.appspot.com"
}

firebase = pyrebase.initialize_app(config)

def stream_handler(message):
    print(message["event"]) # put
    print(message["path"]) # /-K7yGTTEp7O549EzTYtI
    print(message["data"]) # {'title': 'Pyrebase', "body": "etc..."}

#timeout = time.time() + 25
db = firebase.database()

#data = {"mailboxId": 112233, "ocrText":"Frankfurt", "snapshotUrl":"www.zaslujavam.com/a/b/v.jpg"}
#rpushRsult = db.child("MailItems").push(data)
#print(rpushRsult)

my_stream = db.child("MailItems/-LSACc1GVlKHZ5vBZfWK").stream(stream_handler)
time.sleep(30)
my_stream.close()
#while True:
    
    #if time.time() > timeout:
    #    print('timeout')
        #db = firebase.database()
        #data = {"mailboxId": 445566, "ocrText":"Superpalav", "snapshotUrl":"www.izpzpish.com/a/b/v.jpg"}
        #db.child("MailItems").push(data)
        #hmi.sleep()
    #    break
    #elif(proximitySensor.object_in_front()):
        #ubb.start_alarm(1)
        #hmi.idle()
    #    print('after the idle')
        #cam.take_picture()
        #print(imu.uploadImage()['link'])
    #print('Loop')
    #time.sleep(2)

