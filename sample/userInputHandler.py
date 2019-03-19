from cameraSensorManager import CameraSensorManager
from imageUploadManager import ImageUploadManager
from requestExecutionHandler import RequestExecutionHandler
from enums import HmiDisplayPageEnum

class UserInputHandler():

    def __init__(self, hmiDisplayManager):
        self.hmiDisplayManager = hmiDisplayManager
        self.__execute();
    
    def __execute(self):
        try:
            self.hmiDisplayManager.show_page(HmiDisplayPageEnum.TakingPictureOfYou) 
            camera = CameraSensorManager()
            camera.take_picture()
            self.hmiDisplayManager.show_page(HmiDisplayPageEnum.PictureWasTaken)
            
            uploadManager = ImageUploadManager()
            uploadedImageMetadata = uploadManager.uploadImage()
            
            # TODO: Need to bring dynamic behavior here
            ocrParsedText = "OCR"
            
            RequestExecutionHandler(
                self.hmiDisplayManager,
                uploadedImageMetadata['link'],
                ocrParsedText)
            
        except Exception as e:
            raise