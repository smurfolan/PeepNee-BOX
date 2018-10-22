import sys
import serial
import time
import struct
import threading

from patternImplementations import Singleton
from configurationWrapping import GlobalConfigurationWrapper, HmiConfigurationWrapper
from enums import HmiDisplayPageEnum

class HmiDisplayManager():
    __metaclass__ = Singleton
    
    _DAT_FMT_ = 'x6B'
    _HMI_COMMAND_ENDING_ = '\xff\xff\xff'
    _NUMBER_OF_BYTES_TO_READ_ = 7
    _EXPECTED_MIN_SIZE_OF_RECEIVED_PAYLOAD_ = 24
    
    def __init__(self):
        self.configuration = GlobalConfigurationWrapper()
        self.hmiConfiguration = HmiConfigurationWrapper()
        self.serial = serial.Serial(port='/dev/serial0',baudrate=9600,timeout=1.0)
        self.worker_thread = threading.Thread(target=self.__idle_start, args=())
        
    def idle(self):
        if not self.serial.isOpen():
            self.serial.open()
              
        if not self.worker_thread.isAlive():
            self.worker_thread.start()
        
    def sleep(self):
        if hasattr(self, 'worker_thread'):
            self.worker_thread.do_run = False      
    
    def show_page(self, pageId):
        switcher = {
            #TODO: Optimize what is in the argument list of __send_commande
            HmiDisplayPageEnum.Home: lambda: self.__send_command(b'page 0\xff\xff\xff'),
            HmiDisplayPageEnum.GoOnMarkerAndPushAgain: lambda: self.__send_command(b'page 1\xff\xff\xff'),
            HmiDisplayPageEnum.TakingPictureOfYou: lambda: self.__send_command(b'page 2\xff\xff\xff'),
            HmiDisplayPageEnum.WaitingForAnswer: lambda: self.__send_command(b'page 3\xff\xff\xff'),
            HmiDisplayPageEnum.PackageDeclined: lambda: self.__send_command(b'page 4\xff\xff\xff'),
            HmiDisplayPageEnum.PackageAccepted: lambda: self.__send_command(b'page 5\xff\xff\xff'),
            HmiDisplayPageEnum.RepeatTheSteps: lambda: self.__send_command(b'page 6\xff\xff\xff')
        }
        f = switcher.get(pageId, lambda: "Invalid page id")
        f()
            
    # Private methods
    def __send_command(self, command):
        self.serial.write(command)
        
    
    def __idle_start(self):   
        while getattr(self.worker_thread, "do_run", True):
            rcv=self.serial.readline(self._NUMBER_OF_BYTES_TO_READ_)
            if(sys.getsizeof(rcv)>=self._EXPECTED_MIN_SIZE_OF_RECEIVED_PAYLOAD_):
                pageId, btnId, _, _, _, _ = struct.unpack(self._DAT_FMT_, rcv)

                # TODO: Add discrete mechanism for going through the pages
                if(pageId == self.hmiConfiguration.show_package_page_id()):
                    if(btnId == self.hmiConfiguration.show_packge_and_click_button_index()):
                        self.show_page(HmiDisplayPageEnum.TakingPictureOfYou)
                        
            time.sleep(2)
        
        if self.serial.isOpen():
            self.serial.close()