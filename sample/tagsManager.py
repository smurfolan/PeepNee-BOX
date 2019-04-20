import MFRC522
import signal
import time

from patternImplementations import Singleton
from loggingManager import Logger
from firebaseManager import FirebaseManager
from enums import HmiDisplayPageEnum

class TagsManager():
    __metaclass__ = Singleton
    
    def __init__(self):
        self.logger = Logger()
        self.firebaseManager = FirebaseManager()
        
        signal.signal(signal.SIGINT, self.__end_read)
        self.MIFAREReader = MFRC522.MFRC522()
        
        self.tagWasDetected=False
        self.secretCode=''

    def readTags(self, hmiDisplayManager):        
        # Scan for cards    
        (status,TagType) = self.MIFAREReader.MFRC522_Request(self.MIFAREReader.PICC_REQIDL)    
        # Get the UID of the card
        (status,uid) = self.MIFAREReader.MFRC522_Anticoll()

        # If a card is found
        if status == self.MIFAREReader.MI_OK:
            tagId = str(uid[0]) + str(uid[1]) + str(uid[2]) + str(uid[3])
            if tagId:
                self.tagWasDetected = True
                self.__getTagInfoByTagId(tagId)
                hmiDisplayManager.show_page(HmiDisplayPageEnum.KeypadInput)
    
    def isProcessingTag(self):
        return self.tagWasDetected
    
    def appendToSecretCode(self, digit):
        self.secretCode+=str(digit)
    
    def clearInput(self):
        self.secretCode=''
    
    def validateSecretCode(self):
        pass
    
    def __getTagInfoByTagId(self, tagId):
        try:
            tag = self.firebaseManager.get_tag_info_by_tag_id(tagId)
            if tag.val() is not None:
                self.tagSecretCode = tag.val().get('secretCode')
                #Use hmi display manager to show keypad page
            
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