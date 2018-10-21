from imgurpython import ImgurClient

from configurationWrapping import GlobalConfigurationWrapper

class ImageUploadManager():

    def __init__(self):
        self.configuration = GlobalConfigurationWrapper()
        self.clientId = self.configuration.imgur_client_id()
        self.clientSecret = self.configuration.imgur_client_secret()
        self.imagePath = self.configuration.imgur_latest_photo_root_path()
    
    def uploadImage(self):
        try:
            client = ImgurClient(self.clientId, self.clientSecret)
            uploaded_image = client.upload_from_path(self.imagePath, config=None, anon=True)
            
            return uploaded_image
        except BaseException as e:
            print('Error' + str(e))