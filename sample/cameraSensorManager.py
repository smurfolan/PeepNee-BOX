from picamera import PiCamera
from time import sleep

from patternImplementations import Singleton
from configurationWrapping import ConfigurationWrapper

class CameraSensorManager():
    __metaclass__ = Singleton
    
    def __init__(self):
        self.configuration = ConfigurationWrapper()
        self.pathToLatestCapture = self.configuration.imgur_latest_photo_root_path()
            
    def take_picture(self):
        try:
            self.camera = PiCamera()
            self.camera.start_preview()
            sleep(3)
            self.camera.capture(self.pathToLatestCapture, use_video_port=True)
            self.camera.stop_preview()
        finally:
            self.camera.close()