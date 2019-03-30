import RPi.GPIO as GPIO
import time
from pyrebase import pyrebase

from configurationWrapping import GlobalConfigurationWrapper
from patternImplementations import Singleton

class TurnOffRequestHandler():
    __metaclass__ = Singleton
    
    def __init__(self):
        self.configuration = GlobalConfigurationWrapper()
        self.firebaseConfig = {
          "apiKey": self.configuration.fbase_apiKey(),
          "authDomain": self.configuration.fbase_authDomain(),
          "databaseURL": self.configuration.fbase_databaseUrl(),
          "storageBucket": self.configuration.fbase_storageBucket()
        }
        
        self.firebase = pyrebase.initialize_app(self.firebaseConfig)
        self.db = self.firebase.database()
        
        self.turnOffWasRequested = False
        
    def idle(self):
        try:
            self.turn_off_request_stream = self.db.child("Mailboxes/" + self.configuration.box_id()).stream(self.__turn_off_request_stream_handler)
        except BaseException as e:
            self.logger.log_critical('<TurnOffRequestHandler.idle> => ' + str(e))
            raise
    
    def turnOffIsRequested(self):
        return self.turnOffWasRequested
    
    def dispose(self):
        self.turn_off_request_stream.close()
    
    def __turn_off_request_stream_handler(self, message):
        if(message["path"] == '/turnOffRequested' and message["data"] == True):
            self.turnOffWasRequested = True
            time.sleep(3)
            self.db.child("Mailboxes/" + self.configuration.box_id()).update({"turnOffRequested": False})

# Usage example
# torh=TurnOffRequestHandler()
# torh.idle()

# t_end = time.time() + 20
# while time.time() < t_end:
#     if(torh.turnOffIsRequested() == True):
#         print('LETS SHUT THIS BOX DOWN')
#     time.sleep(1)
#     continue

# torh.dispose()
