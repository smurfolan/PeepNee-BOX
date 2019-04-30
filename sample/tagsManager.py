import MFRC522
import signal
import time

from patternImplementations import Singleton
from loggingManager import Logger
from firebaseManager import FirebaseManager
from enums import HmiDisplayPageEnum
from boxOpeningManager import BoxOpeningManager


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
        if hasattr(self, 'boxOpeningManager'):
            del self.boxOpeningManager
        
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
        self.boxOpeningManager=BoxOpeningManager()
        if(self.tagSecretCode == self.secretCodeEntered):
            self.firebaseManager.submit_trusted_mail_item(self.tagOwnerName, self.tagOwnerContact, self.tagCompany)
            self.hmiDisplayManager.show_page(HmiDisplayPageEnum.PackageAccepted)
            self.boxOpeningManager.start_box_opening_procedure()
        else:
            self.hmiDisplayManager.show_page(HmiDisplayPageEnum.PackageDeclined)

        self.clearInput()
        self.tagIsBeingProcessed = False
        time.sleep(3)
        self.hmiDisplayManager.show_page(HmiDisplayPageEnum.Home)
        
    def __getTagInfoByTagId(self, tagId):
        try:
            tag = self.firebaseManager.get_tag_info_by_tag_id(tagId)
            if tag.val() is not None:
                print('TAG INFO WAS FETCHED')
                self.tagSecretCode = str(tag.val().get('secretCode'))
                self.tagOwnerName = str(tag.val().get('owner'))
                self.tagOwnerContact = str(tag.val().get('ownerContact'))
                self.tagCompany = str(tag.val().get('company'))
            
        except BaseException as e:
            self.logger.log_error('<TagsManager.__getTagInfoByTagId> => ' + str(e))
            raise
    
    def __end_read(self, signal,frame):
        print("Ctrl+C captured, ending read.")
        
#tm=TagsManager()
#t_end = time.time() + 25
#while time.time() < t_end and not tm.isProcessingTag():
#    tm.readTags()
#    time.sleep(0.6)    
#print('Reading finished')