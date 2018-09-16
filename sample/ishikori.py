import RPi.GPIO as GPIO
import time

from buzzerSensorManager import BuzzerSensorManager
from proximitySensorManager import ProximitySensorManager
from cameraSensorManager import CameraSensorManager
from imageUploadManager import ImageUploadManager

proximitySensor = ProximitySensorManager()
ubb = BuzzerSensorManager()
cam = CameraSensorManager()
imu = ImageUploadManager()

timeout = time.time() + 20
while True:
    if time.time() > timeout:
        break
    elif(proximitySensor.object_in_front()):
        ubb.start_alarm(1)
        cam.take_picture()
        #print(imu.uploadImage()['link'])