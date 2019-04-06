from firebaseManager import FirebaseManager
from imageUploadManager import ImageUploadManager
from userResponseHandler import UserResponseHandler
from enums import HmiDisplayPageEnum
from soundManager import SoundManager

class RequestExecutionHandler():

    def __init__(self, hmiDisplayManager, imageUrl, ocrParsedText):
            self.hmiDisplayManager = hmiDisplayManager
            self.soundManager = SoundManager()
            
            self.imageUrl = imageUrl
            self.ocrParsedText = ocrParsedText
            
            self.__execute();
    
    def __execute(self):
        try:
            self.soundManager.playSound(SoundEnum.WaitToContactOwner)
            
            fbManager = FirebaseManager()
            imageUploadManager = ImageUploadManager()
            self.hmiDisplayManager.show_page(HmiDisplayPageEnum.WaitingForAnswer)
            imageTags = imageUploadManager.extractImageLabelsByPublicUri(self.imageUrl)
            newMailResponse = fbManager.submit_mail_item(self.ocrParsedText, self.imageUrl, imageTags)
            
            UserResponseHandler(
                self.hmiDisplayManager,
                newMailResponse["mailItemStatus"],
                newMailResponse["openByDefault"])
            
        except Exception as e:
            raise