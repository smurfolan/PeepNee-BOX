import RPi.GPIO as GPIO
import time
from patternImplementations import Singleton

class ProximitySensorManager():
    __metaclass__ = Singleton
    
    __INPUT_GPIO_PIN_NUMBER = 40
    
    def __init__(self):
        GPIO.setmode(GPIO.BOARD)
        GPIO.setup(self.__INPUT_GPIO_PIN_NUMBER, GPIO.IN)
        
    def object_in_front(self):
        sensor = GPIO.input(self.__INPUT_GPIO_PIN_NUMBER)
        return sensor == 0
    
# Usage sample
# psm = ProximitySensorManager()
# timeout = time.time() + 20
# print('You have 20 seconds to test the proximity of the sensor...')
# while True:
#     if time.time() > timeout:         
#         break
#     elif psm.object_in_front():
#         print('OBJECT WAS DETECTED')
#     time.sleep(1)

# print('Proximity sensor detection finished.')