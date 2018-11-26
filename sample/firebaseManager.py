from pyrebase import pyrebase
from configurationWrapping import GlobalConfigurationWrapper
import threading
import time
from enums import MailItemStatus

class FirebaseManager():

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
            data = {
                "mailboxId": self.boxId,
                "ocrText":ocrText,
                "snapshotUrl":snapshotUrl,
                "status": MailItemStatus.Pending
            }
            
            try:
                uploadResult = self.db.child("MailItems").push(data)
                self.referenceToNewlyAddedMailItem = uploadResult['name']
                self.NewlyAddedMailItemStatus = MailItemStatus.Pending
            except BaseException as e:
                pass
            
            if self.referenceToNewlyAddedMailItem is not None:
                print('New item successfully created and stream was created')
                self.new_mail_item_update_stream = self.db.child("MailItems/" + self.referenceToNewlyAddedMailItem).stream(self.__new_mail_item_update_stream_handler)
               
            self.__start_waiting_for_user_response()
        except BaseException as e:
            print('Error' + str(e))
      
    def __new_mail_item_update_stream_handler(self, message):
        #print(message["event"]) # put
        #print(message["path"]) # /-K7yGTTEp7O549EzTYtI
        #print(message["data"]) # {'title': 'Pyrebase', "body": "etc..."}
        if message["path"] == '/status':
            self.NewlyAddedMailItemStatus = message["data"]

    def __start_waiting_for_user_response(self):
        t_end = time.time() + self.timeToWaitBeforeOpenOrClose
        while time.time() < t_end:
            continue

        if self.NewlyAddedMailItemStatus == MailItemStatus.Pending:
            if self.openByDefault:
                print("OPEN BOX") #TODO: Use some opening manager and open the box. Then using hmiDisplayManager show 'Accepted' screen.
                self.db.child("MailItems").child(self.referenceToNewlyAddedMailItem).update({ "status": MailItemStatus.Accepted })
            else:
                print("DO NOTHING. KEEP BOX CLOSED") #TODO: Then using hmiDisplayManager show 'Declined' screen.
                self.db.child("MailItems").child(self.referenceToNewlyAddedMailItem).update({ "status": MailItemStatus.Declined })     
        
        # MailItemStatus.Accepted -> Open the box and update the status on FB. Then using hmiDisplayManager show 'Accepted' screen.
        if self.NewlyAddedMailItemStatus == MailItemStatus.Accepted:
            print("OPEN BOX") #TODO: Use some opening manager and open the box. Then using hmiDisplayManager show 'Accepted' screen.
        
        # MailItemStatus.Declined -> Keep the box closed and update the status on FB. Then using hmiDisplayManager show 'Declined' screen.
        if self.NewlyAddedMailItemStatus == MailItemStatus.Declined:
            print("DO NOTHING. KEEP BOX CLOSED")
        
        # MailItemStatus.Repeat -> Keep the box closed and update the status on FB. Then using hmiDisplayManager show 'Repeat' screen.
        if self.NewlyAddedMailItemStatus == MailItemStatus.Repeat:
            print("REPEAT STEPS") #TODO: Need to change screen from hmiDisplayManager
        
        if self.new_mail_item_update_stream is not None:
            print('Closing update stream..')
            self.new_mail_item_update_stream.close()
    
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
        
#fbm = FirebaseManager()
#fbm.printMe()
#fbm.submit_mail_item("ocre value", "https://i.pinimg.com/236x/29/01/3f/29013f4c4884c0907b9f5694b5bf402b--angry-meme-british.jpg")