from picamera import PiCamera
from time import sleep

from patternImplementations import Singleton
from configurationWrapping import GlobalConfigurationWrapper
from loggingManager import Logger

class CameraSensorManager():
    __metaclass__ = Singleton
    
    def __init__(self):
        self.configuration = GlobalConfigurationWrapper()
        self.pathToLatestCapture = self.configuration.imgur_latest_photo_root_path()
        self.logger = Logger()
            
    def take_picture(self):
        try:
            self.camera = PiCamera()
            self.camera.start_preview()
            sleep(3)
            self.camera.capture(self.pathToLatestCapture, use_video_port=True)
            self.camera.stop_preview()
        except BaseException as e:
            self.logger.log_critical('<CameraSensorManager.take_picture> => ' + str(e))
        finally:
            self.camera.close()
            
# Usage example:
# camera = CameraSensorManager()
# print('About to take a picture...')
# camera.take_picture()
# print('Picture was taken!')