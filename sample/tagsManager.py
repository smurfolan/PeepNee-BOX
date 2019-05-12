import MFRC522
import signal
import time
from pyrebase import pyrebase

from patternImplementations import Singleton
from loggingManager import Logger
from firebaseManager import FirebaseManager
from enums import HmiDisplayPageEnum
from boxOpeningManager import BoxOpeningManager
from configurationWrapping import GlobalConfigurationWrapper


class TagsManager():
    __metaclass__ = Singleton
    __TIMEOUT_PERIOD_IN_SECONDS = 12
    
    def __init__(self):
        self.configuration = GlobalConfigurationWrapper()
        self.requireTwoFactorAuthForTrustedDelivery = self.configuration.box_require_2fa_for_trusted_mail()
        self.boxId = self.configuration.box_id()
        
        self.firebaseConfig = {
          "apiKey": self.configuration.fbase_apiKey(),
          "authDomain": self.configuration.fbase_authDomain(),
          "databaseURL": self.configuration.fbase_databaseUrl(),
          "storageBucket": self.configuration.fbase_storageBucket()
        }
        
        self.firebase = pyrebase.initialize_app(self.firebaseConfig)
        self.db = self.firebase.database()
        
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
            self.__performRfidAcceptance()
        else:
            self.hmiDisplayManager.show_page(HmiDisplayPageEnum.PackageDeclined)
            self.__finishRfidAcceptanceProcedure()

        
    def __getTagInfoByTagId(self, tagId):
        try:
            tag = self.firebaseManager.get_tag_info_by_tag_id(tagId)
            if tag.val() is not None:
                self.__startRfidAcceptanceProcedure(tag.val())
            
        except BaseException as e:
            self.logger.log_error('<TagsManager.__getTagInfoByTagId> => ' + str(e))
            raise
    
    def __startRfidAcceptanceProcedure(self, tagMetadata):
        self.tagSecretCode = str(tagMetadata.get('secretCode'))
        self.tagOwnerName = str(tagMetadata.get('owner'))
        self.tagOwnerContact = str(tagMetadata.get('ownerContact'))
        self.tagCompany = str(tagMetadata.get('company'))
        self.__load_default_settings_from_firebase()
                
        if self.requireTwoFactorAuthForTrustedDelivery:
            self.hmiDisplayManager.show_page(HmiDisplayPageEnum.KeypadInput)
        else:
            self.__performRfidAcceptance()
    
    def __finishRfidAcceptanceProcedure(self):
        self.clearInput()
        self.tagIsBeingProcessed = False
        time.sleep(3)
        self.hmiDisplayManager.show_page(HmiDisplayPageEnum.Home)
    
    def __performRfidAcceptance(self):
        self.boxOpeningManager=BoxOpeningManager()
        self.firebaseManager.submit_trusted_mail_item(self.tagOwnerName, self.tagOwnerContact, self.tagCompany)
        self.hmiDisplayManager.show_page(HmiDisplayPageEnum.PackageAccepted)
        self.boxOpeningManager.start_box_opening_procedure()
        self.__finishRfidAcceptanceProcedure()
    
    def __load_default_settings_from_firebase(self):
        try:
            mailbox = self.db.child("Mailboxes/" + self.boxId).get()
            if mailbox.val() is not None:
                self.requireTwoFactorAuthForTrustedDelivery = mailbox.val().get('requireTwoFactorAuthForTrustedDelivery')
            
        except BaseException as e:
            self.logger.log_error('<TagsManager.__load_default_settings_from_firebase> => ' + str(e))
            raise
    
    def __end_read(self, signal,frame):
        print("Ctrl+C captured, ending read.")
        
#tm=TagsManager()
#t_end = time.time() + 25
#while time.time() < t_end and not tm.isProcessingTag():
#    tm.readTags()
#    time.sleep(0.6)    
#print('Reading finished')