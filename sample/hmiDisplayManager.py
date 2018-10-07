import sys
import serial
import time
import struct
import threading

from patternImplementations import Singleton
from configurationWrapping import ConfigurationWrapper
from enums import HmiDisplayPageEnum

class HmiDisplayManager():
    __metaclass__ = Singleton
    
    _DAT_FMT_ = 'x6B'
    _HMI_COMMAND_ENDING_ = '\xff\xff\xff'
    
    def __init__(self):
        self.configuration = ConfigurationWrapper()
        
        self.serial = serial.Serial(port='/dev/serial0',baudrate=9600,timeout=1.0)
        
        print('Creating new thread')
        self.worker_thread = threading.Thread(target=self.__idle_start, args=())
        
    def idle(self):
        if not self.serial.isOpen():
            print('Open serial port')
            self.serial.open()
              
        if not self.worker_thread.isAlive():
            print('Start worker thread')
            self.worker_thread.start()
        
    def sleep(self):
        if hasattr(self, 'worker_thread'):
            self.worker_thread.do_run = False      
    
    def show_page(self, pageId):
        switcher = {
            #TODO: Optimize what is in the argument list of __send_commande
            HmiDisplayPageEnum.Home: lambda: self.__send_command(b'page page0\xff\xff\xff'),
            HmiDisplayPageEnum.GoOnMarkerAndPushAgain: lambda: self.__send_command(b'page page1\xff\xff\xff'),
            HmiDisplayPageEnum.TakingPictureOfYou: lambda: self.__send_command(b'page page2\xff\xff\xff'),
            HmiDisplayPageEnum.WaitingForAnswer: lambda: self.__send_command(b'page page3\xff\xff\xff'),
            HmiDisplayPageEnum.PackageDeclined: lambda: self.__send_command(b'page page4\xff\xff\xff'),
            HmiDisplayPageEnum.PackageAccepted: lambda: self.__send_command(b'page page5\xff\xff\xff'),
            HmiDisplayPageEnum.RepeatTheSteps: lambda: self.__send_command(b'page page6\xff\xff\xff')
        }
        f = switcher.get(pageId, lambda: "Invalid page id")
        f()
            
    # Private methods
    def __send_command(self, command):
        self.serial.write(command)
        
    
    def __idle_start(self):   
        while getattr(self.worker_thread, "do_run", True):
            rcv=self.serial.readline(7)
            if(sys.getsizeof(rcv)>=24):
                pageId, btnId, _, _, _, _ = struct.unpack(self._DAT_FMT_, rcv)
                # TODO: Add discrete mechanism for going through the pages
                if(pageId == 1):
                    if(btnId == 1):
                        self.show_page(HmiDisplayPageEnum.TakingPictureOfYou)

                print('Button with id:' + str(btnId) + 'on page:' + str(pageId))
                #TODO: Based on buttonId and pageId -> Call the corresponding method.
            time.sleep(2)
        
        if self.serial.isOpen():
            self.serial.close()
            
    
    
            
        