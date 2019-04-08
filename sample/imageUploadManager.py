import requests
from imgurpython import ImgurClient

from configurationWrapping import GlobalConfigurationWrapper
from loggingManager import Logger

class ImageUploadManager():
    __VISION_API_ENDPOINT_URL = 'https://vision.googleapis.com/v1/images:annotate'

    def __init__(self):
        self.configuration = GlobalConfigurationWrapper()
        self.logger = Logger()
        
        self.clientId = self.configuration.imgur_client_id()
        self.clientSecret = self.configuration.imgur_client_secret()
        self.imagePath = self.configuration.imgur_latest_photo_root_path()
            
    def uploadImage(self):
        try:
            client = ImgurClient(self.clientId, self.clientSecret)
            uploaded_image = client.upload_from_path(self.imagePath, config=None, anon=True)
            
            return uploaded_image
        except BaseException as e:
            self.logger.log_critical('<ImageUploadManager.uploadImage> => ' + str(e))

    def extractImageLabelsByPublicUri(self, uri):
        try:
            requestBody = {
                "requests":[
                    {
                        "image":{"source":{"imageUri":uri}},
                        "features":[{"type":"LABEL_DETECTION","maxResults":3}]
                    }
                ]
            }
            
            authParams = {"key": self.configuration.gvapi_apiKey()}
            response = requests.post(self.__VISION_API_ENDPOINT_URL, params=authParams, json=requestBody).json()['responses'][0]['labelAnnotations']
            
            return list(map(lambda x: x['description'], response))          
        except BaseException as e:
            self.logger.log_error('<ImageUploadManager.extractImageLabelsByPublicUri> => ' + str(e))
            raise
        
# Usage example
# ium = ImageUploadManager()
# ium.extractImageLabelsByPublicUri('https://ichef.bbci.co.uk/news/976/cpsprodpb/1363B/production/_89591497_juvenilesaltwater.jpg')
# print('About to upload a picture...')
# urlToUploadedImage = ium.uploadImage()
# print('Picture was uploaded. Its public URL is: ' + str(urlToUploadedImage['link']))