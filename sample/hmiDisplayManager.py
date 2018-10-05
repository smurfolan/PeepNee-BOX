import sys
import serial
import time
import struct
import threading

from patternImplementations import Singleton
from configurationWrapping import ConfigurationWrapper

class HmiDisplayManager():
    __metaclass__ = Singleton
    
    _DAT_FMT_ = 'x6B'
    
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
            
    def __idle_start(self):   
        while getattr(self.worker_thread, "do_run", True):
            rcv=self.serial.readline(10)
            if(sys.getsizeof(rcv)==24):
                pageId, btnId, _, _, _, _ = struct.unpack(self._DAT_FMT_, rcv)
                print('Button with id:' + str(btnId) + 'on page:' + str(pageId))
            time.sleep(2)
        
        if self.serial.isOpen():
            print('Closing serial')
            self.serial.close()
            
    
    
            
        