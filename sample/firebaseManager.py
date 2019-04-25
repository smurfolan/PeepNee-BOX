from pyrebase import pyrebase
from configurationWrapping import GlobalConfigurationWrapper
import threading
import time
import datetime
import email.utils
from enums import MailItemStatus

from loggingManager import Logger

class FirebaseManager():
    # Additional seconds are added because of the network latency.
    __NETWORK_LATENCY_COMPROMISE_SECONDS = 4

    def __init__(self):
        self.configuration = GlobalConfigurationWrapper()
        self.logger = Logger()
        
        self.firebaseConfig = {
          "apiKey": self.configuration.fbase_apiKey(),
          "authDomain": self.configuration.fbase_authDomain(),
          "databaseURL": self.configuration.fbase_databaseUrl(),
          "storageBucket": self.configuration.fbase_storageBucket()
        }
        
        self.firebase = pyrebase.initialize_app(self.firebaseConfig)
        self.db = self.firebase.database()
        
        self.__load_local_default_settings()
        self.__load_default_settings_from_firebase()
        
    def submit_anonymous_mail_item(self, ocrText, snapshotUrl, associatedImageTags):
        try:
            mailReceivedAt = datetime.datetime.now(datetime.timezone.utc)
            waitForUserResponseUntil = email.utils.format_datetime(mailReceivedAt + datetime.timedelta(seconds=int(self.timeToWaitBeforeOpenOrClose) + self.__NETWORK_LATENCY_COMPROMISE_SECONDS))
            numberOfImageTags = len(associatedImageTags)
            data = {
                "mailboxId": (int)(self.boxId),
                "ocrText":ocrText,
                "snapshotUrl":snapshotUrl,
                "status": MailItemStatus.Pending,
                "receivedAt": email.utils.format_datetime(mailReceivedAt),
                "waitForResponseUntil": waitForUserResponseUntil,
                "topScoreImageTag": associatedImageTags[0] if numberOfImageTags > 0 else "",
                "middleScoreImageTag": associatedImageTags[1] if numberOfImageTags > 1 else "",
                "lowestScoreImageTag": associatedImageTags[2] if numberOfImageTags > 2 else "",
                "isAnonymous": True
            }
            
            try:
                uploadResult = self.db.child("MailItems").push(data)
                self.referenceToNewlyAddedMailItem = uploadResult['name']
                self.NewlyAddedMailItemStatus = MailItemStatus.Pending
            except BaseException as e:
                pass
            
            if self.referenceToNewlyAddedMailItem is not None:
                self.logger.log_information('<FirebaseManager.__start_waiting_for_user_response> => New item successfully created and stream was created')
                self.new_mail_item_update_stream = self.db.child("MailItems/" + self.referenceToNewlyAddedMailItem).stream(self.__new_mail_item_update_stream_handler)
               
            newMailItemStatus = self.__start_waiting_for_user_response()
            
            return {
                    "mailItemStatus": newMailItemStatus,
                    "openByDefault": self.openByDefault
                    }
        except BaseException as e:
            self.logger.log_critical('<FirebaseManager.submit_anonymous_mail_item> => ' + str(e))
            raise
    
    def submit_trusted_mail_item(self, tagOwnerName, tagOwnerContact, tagCompany):
        try:
            mailReceivedAt = datetime.datetime.now(datetime.timezone.utc)
            data = {
                "mailboxId": (int)(self.boxId),
                "receivedAt": email.utils.format_datetime(mailReceivedAt),
                "rfidCompany": tagCompany,
                "rfidTagOwner": tagOwnerName,
                "rfidTagOwnerContact": tagOwnerContact,
                "isAnonymous": False
            }
            self.db.child("MailItems").push(data)         
        except BaseException as e:
            self.logger.log_critical('<FirebaseManager.submit_trusted_mail_item> => ' + str(e))
            raise 
    
    def toggle_mailbox_active_status(self, isActive):
        try:
            self.db.child("Mailboxes").child(self.boxId).update({"isActive": isActive})
        except BaseException as e:
            self.logger.log_critical('<FirebaseManager.toggle_mailbox_active_status> => ' + str(e))
            raise
    
    def get_tag_info_by_tag_id(self, tagId):
        try:
            return self.db.child("Tags/" + tagId).get()
        except BaseException as e:
            self.logger.log_error('<FirebaseManager.get_tag_info_by_tag_id> => ' + str(e))
            raise
    
    def __new_mail_item_update_stream_handler(self, message):
        if message["data"] is not None and message["data"]["status"] is not None:
            self.NewlyAddedMailItemStatus = int(message["data"]["status"])

    def __start_waiting_for_user_response(self):
        t_end = time.time() + self.timeToWaitBeforeOpenOrClose + self.__NETWORK_LATENCY_COMPROMISE_SECONDS
        while time.time() < t_end:
            continue

        if self.NewlyAddedMailItemStatus == MailItemStatus.Pending:
            if self.openByDefault:
                self.db.child("MailItems").child(self.referenceToNewlyAddedMailItem).update({ "status": MailItemStatus.Accepted })
            else:
                self.db.child("MailItems").child(self.referenceToNewlyAddedMailItem).update({ "status": MailItemStatus.Declined })     
        
        if self.new_mail_item_update_stream is not None:
            self.logger.log_information('<FirebaseManager.__start_waiting_for_user_response> => Closing update stream..')
            self.new_mail_item_update_stream.close()
            
        return self.NewlyAddedMailItemStatus
            
    def __load_default_settings_from_firebase(self):
        try:
            mailbox = self.db.child("Mailboxes/" + self.boxId).get()
            if mailbox.val() is not None:
                self.openByDefault = mailbox.val().get('openByDefault')
                self.timeToWaitBeforeOpenOrClose = mailbox.val().get('timeToWaitBeforeOpenOrClose')
            
        except BaseException as e:
            self.logger.log_error('<FirebaseManager.__load_default_settings_from_firebase> => ' + str(e))
            raise
    
    def __load_local_default_settings(self):
        self.boxId = self.configuration.box_id()
        self.openByDefault = self.configuration.box_open_by_default()
        self.timeToWaitBeforeOpenOrClose = self.configuration.box_time_to_wait_before_open_or_close()

# Usage example
# fbm = FirebaseManager()
# fbm.toggle_mailbox_active_status(True)
# fbm.submit_mail_item("ocre value", "https://i.pinimg.com/236x/29/01/3f/29013f4c4884c0907b9f5694b5bf402b--angry-meme-british.jpg", ["car", "vehicle", "police"])