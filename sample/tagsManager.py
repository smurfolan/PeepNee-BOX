import MFRC522
import signal
import time

from patternImplementations import Singleton
from loggingManager import Logger
from firebaseManager import FirebaseManager
from enums import HmiDisplayPageEnum

class TagsManager():
    __metaclass__ = Singleton
    __TIMEOUT_PERIOD_IN_SECONDS = 12
    
    def __init__(self):
        self.logger = Logger()
        self.firebaseManager = FirebaseManager()
        
        signal.signal(signal.SIGINT, self.__end_read)
        self.MIFAREReader = MFRC522.MFRC522()
        
        self.tagIsBeingProcessed=False
        self.secretCodeEntered=''
        self.lastDetectionDateTime=0

    def readTags(self, hmiDisplayManager):
        self.hmiDisplayManager = hmiDisplayManager
        # Scan for cards    
        (status,TagType) = self.MIFAREReader.MFRC522_Request(self.MIFAREReader.PICC_REQIDL)    
        # Get the UID of the card
        (status,uid) = self.MIFAREReader.MFRC522_Anticoll()

        # If a card is found
        if status == self.MIFAREReader.MI_OK:
            tagId = str(uid[0]) + str(uid[1]) + str(uid[2]) + str(uid[3])
            if tagId:
                self.lastDetectionDateTime = int(time.time())
                self.tagIsBeingProcessed = True
                self.__getTagInfoByTagId(tagId)
                self.hmiDisplayManager.show_page(HmiDisplayPageEnum.KeypadInput)
        
    def isProcessingTag(self):
        timeout = int(time.time())-self.lastDetectionDateTime >= self.__TIMEOUT_PERIOD_IN_SECONDS
        if(timeout):
            self.tagIsBeingProcessed=False

        return self.tagIsBeingProcessed
    
    def appendToSecretCode(self, digit):
        self.secretCodeEntered+=str(digit)
    
    def clearInput(self):
        self.secretCodeEntered=''
    
    def validateSecretCode(self):
        if(self.tagSecretCode == self.secretCodeEntered):
            print('Secret code is valid')
        else:
            print('Secret code is not valid')
        
        self.hmiDisplayManager.show_page(HmiDisplayPageEnum.Home)
        self.clearInput()
        self.tagIsBeingProcessed = False
    
    def __getTagInfoByTagId(self, tagId):
        try:
            tag = self.firebaseManager.get_tag_info_by_tag_id(tagId)
            if tag.val() is not None:
                self.tagSecretCode = str(tag.val().get('secretCode'))
            
        except BaseException as e:
            self.logger.log_error('<TagsManager.__getTagInfoByTagId> => ' + str(e))
            raise
    
    def __end_read(signal,frame):
        print("Ctrl+C captured, ending read.")
        
#tm=TagsManager()
#t_end = time.time() + 25
#while time.time() < t_end and not tm.isProcessingTag():
#    tm.readTags()
#    time.sleep(0.6)    
#print('Reading finished')