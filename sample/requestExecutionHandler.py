from firebaseManager import FirebaseManager
from userResponseHandler import UserResponseHandler
from enums import HmiDisplayPageEnum

class RequestExecutionHandler():

    def __init__(self, hmiDisplayManager, imageUrl, ocrParsedText):
            self.hmiDisplayManager = hmiDisplayManager
            
            self.imageUrl = imageUrl
            self.ocrParsedText = ocrParsedText
            
            self.__execute();
    
    def __execute(self):
        try:
            fbManager = FirebaseManager()
            self.hmiDisplayManager.show_page(HmiDisplayPageEnum.WaitingForAnswer)
            newMailResponse = fbManager.submit_mail_item(self.ocrParsedText, self.imageUrl)
            
            UserResponseHandler(
                self.hmiDisplayManager,
                newMailResponse["mailItemStatus"],
                newMailResponse["openByDefault"])
            
        except Exception as e:
            raise