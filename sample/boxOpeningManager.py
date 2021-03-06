from servoManager import ServoManager
from proximitySensorManager import ProximitySensorManager
from configurationWrapping import GlobalConfigurationWrapper
from loggingManager import Logger

import time

class BoxOpeningManager():

    def __init__(self):
        self.configuration = GlobalConfigurationWrapper()
        self.timeToKeepTheBoxOpen = self.configuration.box_time_to_keep_the_box_open()
        self.logger = Logger()
        
        self.servoManager = ServoManager()      
        self.proximitySensorManager = ProximitySensorManager();
        
    def start_box_opening_procedure(self):
        try:
            self.servoManager.openMailbox()
        
            t_end = time.time() + (int)(self.timeToKeepTheBoxOpen)
            while time.time() < t_end:
                continue

            while True:
                if not self.proximitySensorManager.object_in_front() :         
                    self.servoManager.closeMailbox()
                    break;
                else :
                    time.sleep(1)
        except BaseException as e:
            self.logger.log_critical('<BoxOpeningManager.start_box_opening_procedure> => ' + str(e))
            
# Usage example
# bom = BoxOpeningManager()
# bom.start_box_opening_procedure()