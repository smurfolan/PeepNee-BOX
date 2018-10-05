import sys
import serial
import time
import struct

from patternImplementations import Singleton
from configurationWrapping import ConfigurationWrapper

class HmiDisplayManager():
    __metaclass__ = Singleton
    
    DAT_FMT = 'x6B'
    
    def __init__(self):
        self.configuration = ConfigurationWrapper()
        self.serial = serial.Serial(port='/dev/serial0',baudrate=9600,timeout=1.0)
        self.in_idle_state = False
            
    def idle(self):
        self.in_idle_stat = True
        
        while self.in_idle_stat:
            print("Read line")
            rcv=ser.readline(10)
            if(sys.getsizeof(rcv)==24):
                pageId, btnId, _, _, _, _ = struct.unpack(DAT_FMT, rcv)
                print('Button with id:' + str(btnId) + 'on page:' + str(pageId))
            time.sleep(2)
    
    def hibernate(self):
        self.in_idle_stat = False