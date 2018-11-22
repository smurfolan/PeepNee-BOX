from pyrebase import pyrebase
from configurationWrapping import GlobalConfigurationWrapper

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
        
    def printMe(self):
        print('Box id:' + str(self.boxId) + ', openByDefault:' + str(self.openByDefault) + ', timeToWaitBeforeOpenOrClose:' + str(self.timeToWaitBeforeOpenOrClose))

fbm = FirebaseManager()
fbm.printMe()