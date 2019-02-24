import RPi.GPIO as GPIO
from time import sleep
import datetime
import subprocess

from patternImplementations import Singleton
from firebaseManager import FirebaseManager

class UpsManager():
    __metaclass__ = Singleton
    
    __INPUT_GPIO_PIN_NUMBER = 11
    __CHECK_FREQUENCY = 5
    __MINIMAL_LOW_BAT_DET_TIMEGAP_ALLOWED = 5.5
    __LOG_FILE_NAME = "lowBatteryLog.txt"
    
    def __init__(self):
        GPIO.setmode(GPIO.BOARD)
        GPIO.setup(self.__INPUT_GPIO_PIN_NUMBER, GPIO.IN)
        self._lastTimeLowBatteryDetected = None
       
    def periodicallyCheckBatteryLevel(self):
        while True:
            # -- Low battery was detected -- #
            if not GPIO.input(self.__INPUT_GPIO_PIN_NUMBER):
                self.__log_low_battery_entry()
                
                if self._lastTimeLowBatteryDetected is None:
                    self._lastTimeLowBatteryDetected = datetime.datetime.now(datetime.timezone.utc)
                else:
                    utcDatetimeNow = datetime.datetime.now(datetime.timezone.utc)
                    lowBatteryDetectionsTimeGap = (utcDatetimeNow - self._lastTimeLowBatteryDetected).total_seconds()
                    if lowBatteryDetectionsTimeGap <= self.__MINIMAL_LOW_BAT_DET_TIMEGAP_ALLOWED:
                        self.__start_shutdown_procedure()
                    else:
                        self._lastTimeLowBatteryDetected = utcDatetimeNow
            sleep(self.__CHECK_FREQUENCY)

    def __start_shutdown_procedure(self):
        f = open(self.__LOG_FILE_NAME, "a")
        f.write("The mailbox is going to shut down now!\n")
        f.close()
        
        fbManager = FirebaseManager()
        fbManager.toggle_mailbox_active_status(False)
        
        subprocess.call(["sudo","shutdown","-h","now"])
            
    def __log_low_battery_entry(self):
        f = open(self.__LOG_FILE_NAME, "a")
        f.write("[" + str(datetime.datetime.now()) + "] LOW BATTERY!\n")
        f.close()

# Usage example
# upsm=UpsManager()
# sleep(2)
# upsm.periodicallyCheckBatteryLevel()


