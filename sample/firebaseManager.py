from pyrebase import pyrebase
from configurationWrapping import GlobalConfigurationWrapper
import threading
import time
import datetime
import email.utils
from enums import MailItemStatus

class FirebaseManager():
    # Additional seconds are added because of the network latency.
    __NETWORK_LATENCY_COMPROMISE_SECONDS = 4

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
        
        self.__load_local_default_settings()
        self.__load_default_settings_from_firebase()
        
    def submit_mail_item(self, ocrText, snapshotUrl):
        try:
            mailReceivedAt = datetime.datetime.now(datetime.timezone.utc)
            waitForUserResponseUntil = email.utils.format_datetime(mailReceivedAt + datetime.timedelta(seconds=int(self.timeToWaitBeforeOpenOrClose) + self.__NETWORK_LATENCY_COMPROMISE_SECONDS))
            data = {
                "mailboxId": (int)(self.boxId),
                "ocrText":ocrText,
                "snapshotUrl":snapshotUrl,
                "status": MailItemStatus.Pending,
                "receivedAt": email.utils.format_datetime(mailReceivedAt),
                "waitForResponseUntil": waitForUserResponseUntil
            }
            
            try:
                uploadResult = self.db.child("MailItems").push(data)
                self.referenceToNewlyAddedMailItem = uploadResult['name']
                self.NewlyAddedMailItemStatus = MailItemStatus.Pending
            except BaseException as e:
                pass
            
            if self.referenceToNewlyAddedMailItem is not None:
                print('[DEBUG] New item successfully created and stream was created')
                self.new_mail_item_update_stream = self.db.child("MailItems/" + self.referenceToNewlyAddedMailItem).stream(self.__new_mail_item_update_stream_handler)
               
            newMailItemStatus = self.__start_waiting_for_user_response()
            
            return {
                    "mailItemStatus": newMailItemStatus,
                    "openByDefault": self.openByDefault
                    }
        except BaseException as e:
            print('Error' + str(e))
      
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
            print('[DEBUG]: Closing update stream..')
            self.new_mail_item_update_stream.close()
            
        return self.NewlyAddedMailItemStatus
            
    def __load_default_settings_from_firebase(self):
        try:
            mailbox = self.db.child("Mailboxes/" + self.boxId).get()
            if mailbox.val() is not None:
                self.openByDefault = mailbox.val().get('openByDefault')
                self.timeToWaitBeforeOpenOrClose = mailbox.val().get('timeToWaitBeforeOpenOrClose')
            
        except BaseException as e:
            print('Error' + str(e))
    
    def __load_local_default_settings(self):
        self.boxId = self.configuration.box_id()
        self.openByDefault = self.configuration.box_open_by_default()
        self.timeToWaitBeforeOpenOrClose = self.configuration.box_time_to_wait_before_open_or_close()

# Usage example
# fbm = FirebaseManager()
# fbm.submit_mail_item("ocre value", "https://i.pinimg.com/236x/29/01/3f/29013f4c4884c0907b9f5694b5bf402b--angry-meme-british.jpg")