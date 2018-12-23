from enums import MailItemStatus
from enums import HmiDisplayPageEnum

from boxOpeningManager import BoxOpeningManager

class UserResponseHandler():

    def __init__(self, hmiDisplayManager, mailItemStatus, openByDefault):
            self.hmiDisplayManager = hmiDisplayManager
            self.mailItemStatus = mailItemStatus
            self.openByDefault = openByDefault
            
            self.boxOpeningManager = BoxOpeningManager()
        
            self.__execute();
    
    def __execute(self):
        try:
            if self.mailItemStatus == MailItemStatus.Pending:
                if self.openByDefault:
                    self.hmiDisplayManager.show_page(HmiDisplayPageEnum.PackageAccepted)
                    self.boxOpeningManager.start_box_opening_procedure()
                else:
                    self.hmiDisplayManager.show_page(HmiDisplayPageEnum.PackageDeclined)   
        
            if self.mailItemStatus == MailItemStatus.Accepted:
                self.hmiDisplayManager.show_page(HmiDisplayPageEnum.PackageAccepted)
                self.boxOpeningManager.start_box_opening_procedure()
        
            if self.mailItemStatus == MailItemStatus.Declined:
                self.hmiDisplayManager.show_page(HmiDisplayPageEnum.PackageDeclined)

            if self.mailItemStatus == MailItemStatus.Repeat:
                self.hmiDisplayManager.show_page(HmiDisplayPageEnum.RepeatTheSteps)
                
        except Exception as e:
            raise