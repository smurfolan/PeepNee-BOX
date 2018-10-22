import RPi.GPIO as GPIO
import time
import serial

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

timeout = time.time() + 25
while True:
    if time.time() > timeout:
        print('timeout')
        hmi.sleep()
        break
    elif(proximitySensor.object_in_front()):
        #ubb.start_alarm(1)
        hmi.idle()
        #print('after the idle')
        #cam.take_picture()
        #print(imu.uploadImage()['link'])
    print('Loop')
    time.sleep(2)

