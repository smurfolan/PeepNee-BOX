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