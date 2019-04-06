import pygame

from loggingManager import Logger
from enums import SoundEnum

class SoundManager():
    __SOUND_FILES_ROOT = '/home/pi/Desktop/PeepNee/sample/sounds/'

    def __init__(self):
        pygame.init()
        self.logger = Logger()
        
    def playSound(self, soundId):
        self.__loadSound(soundId)
        self.__playLoadedSound()
    
    def __loadSound(self, soundId):
        try:
            switcher = {
                SoundEnum.Hello:
                    lambda: pygame.mixer.music.load(self.__SOUND_FILES_ROOT + 'Alice_Hello.wav'),        
                SoundEnum.ClickOnCapture:
                    lambda: pygame.mixer.music.load(self.__SOUND_FILES_ROOT + 'Alice_ClickOnCapture.wav'),         
                SoundEnum.WaitToContactOwner:
                    lambda: pygame.mixer.music.load(self.__SOUND_FILES_ROOT + 'Alice_WaitToContactOwner.wav'),              
                SoundEnum.PackageAccepted:
                    lambda: pygame.mixer.music.load(self.__SOUND_FILES_ROOT + 'Alice_PackageAccepted.wav'),          
                SoundEnum.PackageDeclined:
                    lambda: pygame.mixer.music.load(self.__SOUND_FILES_ROOT + 'Alice_PackageDeclined.wav'),              
                SoundEnum.OwnerRequestedRepeat:
                    lambda: pygame.mixer.music.load(self.__SOUND_FILES_ROOT + 'Alice_OwnerRequestedRepeat.wav'),         
                SoundEnum.ThankYou:
                    lambda: pygame.mixer.music.load(self.__SOUND_FILES_ROOT + 'Alice_ThankYou.wav')
            }
            f = switcher.get(soundId, lambda: "Invalid sound id")
            f()
        except BaseException as e:
            self.logger.log_critical('<SoundManager.__loadSound> => ' + str(e))
    
    def __playLoadedSound(self):
        pygame.mixer.music.play(0)
    
    def __stopSound(self):
        pygame.mixer.music.stop()
        
# Usage example
# sm = SoundManager()
# sm.playSound(SoundEnum.OwnerRequestedRepeat)
