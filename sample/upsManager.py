import RPi.GPIO as GPIO
from time import sleep
import datetime
import subprocess
import threading

from patternImplementations import Singleton
from firebaseManager import FirebaseManager
from loggingManager import Logger

class UpsManager():
    __metaclass__ = Singleton
    
    __INPUT_GPIO_PIN_NUMBER = 11
    __CHECK_FREQUENCY = 5
    __MINIMAL_LOW_BAT_DET_TIMEGAP_ALLOWED = 5.5
    __LOG_FILE_NAME = "/home/pi/Desktop/PeepNee/sample/lowBatteryLog.txt"
    
    def __init__(self):
        GPIO.setmode(GPIO.BOARD)
        GPIO.setup(self.__INPUT_GPIO_PIN_NUMBER, GPIO.IN)
        self._lastTimeLowBatteryDetected = None
        
        self.worker_thread = threading.Thread(target=self.__periodicallyCheckBatteryLevel, args=())
        self.logger = Logger()
     
    def idle(self):
        try:
            if not self.worker_thread.isAlive():
                self.worker_thread.start()
        except BaseException as e:
            self.logger.log_critical('<UpsManager.idle> => ' + str(e))
            raise
    
    def sleep(self):
        try:
            if hasattr(self, 'worker_thread'):
                self.worker_thread.do_run = False
        except BaseException as e:
            self.logger.log_critical('<UpsManager.sleep> => ' + str(e))
     
    def __periodicallyCheckBatteryLevel(self):
        try:
            while getattr(self.worker_thread, "do_run", True):
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
        except BaseException as e:
            self.logger.log_critical('<UpsManager.__periodicallyCheckBatteryLevel> => ' + str(e))

    def __start_shutdown_procedure(self):
        f = open(self.__LOG_FILE_NAME, "a")
        f.write("The mailbox is going to shut down now!\n")
        f.flush()
        f.close()
        
        fbManager = FirebaseManager()
        fbManager.toggle_mailbox_active_status(False)
        
        subprocess.call(["sudo","shutdown","-h","now"])
            
    def __log_low_battery_entry(self):
        f = open(self.__LOG_FILE_NAME, "a")
        f.write("[" + str(datetime.datetime.now()) + "] LOW BATTERY!\n")
        f.flush()
        f.close()

# Usage example
# upsm=UpsManager()
# upsm.idle()
# print('UPS manager is now in idle state.')
# sleep(40)
# upsm.sleep()
# print('UPS manager is now in sleep state.')