from enum import IntEnum

class ErrorLevelEnum(IntEnum):
    Information = 2
    Error = 4
    Critical = 5

class LogToEnum(IntEnum):
    Console = 1
    File = 2
    
class HmiDisplayPageEnum:
    Home = 0
    GoOnMarkerAndPushAgain = 1
    TakingPictureOfYou = 2
    WaitingForAnswer = 3
    PackageDeclined = 4
    PackageAccepted = 5
    RepeatTheSteps = 6
    ThankYou = 7
    PictureWasTaken = 8
    KeypadInput = 9
    
class SoundEnum:
    Hello = 0
    ClickOnCapture = 1
    WaitToContactOwner = 2
    PackageAccepted = 3   
    PackageDeclined = 4
    OwnerRequestedRepeat = 5
    ThankYou = 6
    
class MailItemStatus(IntEnum):
    Pending = 2
    Accepted = 1
    Declined = 0
    Repeat = 3