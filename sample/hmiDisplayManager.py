import sys
import serial
import time
import struct
import threading

from patternImplementations import Singleton
from configurationWrapping import GlobalConfigurationWrapper, HmiConfigurationWrapper
from enums import HmiDisplayPageEnum

from userInputHandler import UserInputHandler
from boxOpeningManager import BoxOpeningManager

class HmiDisplayManager():
    __metaclass__ = Singleton
    
    _DAT_FMT_ = 'x6B'
    _HMI_COMMAND_ENDING_ = '\xff\xff\xff'
    _NUMBER_OF_BYTES_TO_READ_ = 7
    _EXPECTED_MIN_SIZE_OF_RECEIVED_PAYLOAD_ = 24
    
    def __init__(self):
        self.configuration = GlobalConfigurationWrapper()
        self.hmiConfiguration = HmiConfigurationWrapper()
        self.boxOpeningManager = BoxOpeningManager()
        
        self.serial = serial.Serial(port='/dev/serial0',baudrate=9600,timeout=1.0)
        self.worker_thread = threading.Thread(target=self.__idle_start, args=())
        
    def idle(self):
        self.show_page(HmiDisplayPageEnum.Home)
        
        if not self.serial.isOpen():
            self.serial.open()
              
        if not self.worker_thread.isAlive():
            self.worker_thread.start()
        
    def sleep(self):
        if hasattr(self, 'worker_thread'):
            self.worker_thread.do_run = False      
    
    def show_page(self, pageId):
        switcher = {
            HmiDisplayPageEnum.Home:
                lambda: self.__send_command(self.__formatted_page_command(self.hmiConfiguration.home_page_id())),
            HmiDisplayPageEnum.GoOnMarkerAndPushAgain:
                lambda: self.__send_command(self.__formatted_page_command(self.hmiConfiguration.show_package_page_id())),
            HmiDisplayPageEnum.TakingPictureOfYou:
                lambda: self.__send_command(self.__formatted_page_command(self.hmiConfiguration.taking_picture_page_id())),
            HmiDisplayPageEnum.WaitingForAnswer:
                lambda: self.__send_command(self.__formatted_page_command(self.hmiConfiguration.wait_page_id())),
            HmiDisplayPageEnum.PackageDeclined:
                lambda: self.__send_command(self.__formatted_page_command(self.hmiConfiguration.packageDeclinedPageId())),
            HmiDisplayPageEnum.PackageAccepted:
                lambda: self.__send_command(self.__formatted_page_command(self.hmiConfiguration.package_accepted_page_id())),
            HmiDisplayPageEnum.RepeatTheSteps:
                lambda: self.__send_command(self.__formatted_page_command(self.hmiConfiguration.repeat_steps_page_id())),
            HmiDisplayPageEnum.ThankYou:
                lambda: self.__send_command(self.__formatted_page_command(self.hmiConfiguration.thank_you_page_id()))
        }
        f = switcher.get(pageId, lambda: "Invalid page id")
        f()
            
    # Private methods
    def __send_command(self, command):
        self.serial.write(command)
        
    def __formatted_page_command(self, pageId):
        # This the representation of 'page 0\xff\xff\xff'. What we do here is to dynamically assign the page id.
        commandAsBytesArray = [0x70,0x61,0x67,0x65,0x20,0x30,0xff, 0xff, 0xff]
        commandAsBytesArray[5] = ord(str(pageId))
        return bytes(commandAsBytesArray)
    # TODO: Avoid this 'Christmas tree' issue.
    def __idle_start(self):   
        while getattr(self.worker_thread, "do_run", True):
            rcv=self.serial.readline(self._NUMBER_OF_BYTES_TO_READ_)
            if(sys.getsizeof(rcv)>=self._EXPECTED_MIN_SIZE_OF_RECEIVED_PAYLOAD_):
                pageId, btnId, _, _, _, _ = struct.unpack(self._DAT_FMT_, rcv)

                # TODO: Add discrete mechanism for going through the pages
                if(pageId == self.hmiConfiguration.show_package_page_id()):
                    if(btnId == self.hmiConfiguration.show_packge_and_click_button_index()):
                        try:
                            UserInputHandler(self)
                        except Exception as e:
                            #send_somewhere(traceback.format_exception(*sys.exc_info()))                         
                            self.show_page(HmiDisplayPageEnum.PackageAccepted)
                            self.boxOpeningManager.start_box_opening_procedure()
            time.sleep(2)
        
        if self.serial.isOpen():
            self.serial.close()

# Usage example
# hmi = HmiDisplayManager()
# hmi.show_page(HmiDisplayPageEnum.Home)
# hmi.idle()
# print('Hmi display is now in idle state.')
# time.sleep(40)
# hmi.sleep()
# print('Hmi display is now in sleep state.')