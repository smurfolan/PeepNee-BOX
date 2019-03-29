import RPi.GPIO as GPIO
from time import sleep

from patternImplementations import Singleton
from loggingManager import Logger

class ServoManager():
    __metaclass__ = Singleton
    
    __OUTPUT_GPIO_PIN_NUMBER = 12
    
    def __init__(self):
        GPIO.setmode(GPIO.BOARD)#Numbers GPIOs by physical location
        GPIO.setup(self.__OUTPUT_GPIO_PIN_NUMBER, GPIO.OUT)
        
        self.pwm=GPIO.PWM(self.__OUTPUT_GPIO_PIN_NUMBER,50)
        self.pwm.start(0)
        
        self.logger = Logger()
    
    def openMailbox(self):
        try:
            self.__set_angle(13)
        except BaseException as e:
            self.logger.log_critical('<ServoManager.openMailbox> => ' + str(e))
    
    def closeMailbox(self):
        try:
            self.__set_angle(185)
        except BaseException as e:
            self.logger.log_critical('<ServoManager.closeMailbox> => ' + str(e))
    
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