import time

from enums import MailItemStatus
from enums import HmiDisplayPageEnum, SoundEnum

from boxOpeningManager import BoxOpeningManager
from soundManager import SoundManager

class UserResponseHandler():

    def __init__(self, hmiDisplayManager, mailItemStatus, openByDefault):
            self.hmiDisplayManager = hmiDisplayManager
            self.mailItemStatus = mailItemStatus
            self.openByDefault = openByDefault
            
            self.boxOpeningManager = BoxOpeningManager()
            self.soundManager = SoundManager()
        
            self.__execute();
    
    def __execute(self):
        try:
            if self.mailItemStatus == MailItemStatus.Repeat:
                self.soundManager.playSound(SoundEnum.OwnerRequestedRepeat)
                self.hmiDisplayManager.show_page(HmiDisplayPageEnum.RepeatTheSteps)
                time.sleep(3)
                self.hmiDisplayManager.show_page(HmiDisplayPageEnum.GoOnMarkerAndPushAgain)
            else:   
                if (self.mailItemStatus == MailItemStatus.Pending and self.openByDefault) or self.mailItemStatus == MailItemStatus.Accepted:
                    self.soundManager.playSound(SoundEnum.PackageAccepted)
                    self.hmiDisplayManager.show_page(HmiDisplayPageEnum.PackageAccepted)
                    self.boxOpeningManager.start_box_opening_procedure()
                
                if (self.mailItemStatus == MailItemStatus.Pending and not self.openByDefault) or self.mailItemStatus == MailItemStatus.Declined:
                    self.soundManager.playSound(SoundEnum.PackageDeclined)
                    self.hmiDisplayManager.show_page(HmiDisplayPageEnum.PackageDeclined)
                    time.sleep(6)
        
                self.__finish_the_flow()               
        except Exception as e:
            raise
        
    def __finish_the_flow(self):
        self.hmiDisplayManager.show_page(HmiDisplayPageEnum.ThankYou)
        self.soundManager.playSound(SoundEnum.ThankYou)