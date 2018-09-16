from enum import IntEnum

class ErrorLevelEnum(IntEnum):
    Information = 2
    Error = 4
    Critical = 5

class LogToEnum(IntEnum):
    Console = 1
    File = 2