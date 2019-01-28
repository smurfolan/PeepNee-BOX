import RPi.GPIO as GPIO
from time import sleep

from patternImplementations import Singleton

class ServoManager():
    __metaclass__ = Singleton
    
    __OUTPUT_GPIO_PIN_NUMBER = 12
    
    def __init__(self):
        GPIO.setmode(GPIO.BOARD)#Numbers GPIOs by physical location
        GPIO.setup(self.__OUTPUT_GPIO_PIN_NUMBER, GPIO.OUT)
        
        self.pwm=GPIO.PWM(self.__OUTPUT_GPIO_PIN_NUMBER,50)
        self.pwm.start(0)
    
    def openMailbox(self):
        self.__set_angle(13)
    
    def closeMailbox(self):
        self.__set_angle(185)
    
    def __set_angle(self, angle):
        duty = (angle/18 + 2)
        
        GPIO.output(self.__OUTPUT_GPIO_PIN_NUMBER, True)
        self.pwm.ChangeDutyCycle(duty)
        
        sleep(1)
        
        GPIO.output(self.__OUTPUT_GPIO_PIN_NUMBER, False)
        self.pwm.ChangeDutyCycle(0)

# Usage example
# sm=ServoManager()
# sm.openMailbox()
# sleep(10)
# sm.closeMailbox()