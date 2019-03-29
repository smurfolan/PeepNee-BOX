import sys
from configurationWrapping import GlobalConfigurationWrapper
from patternImplementations import Singleton
from enums import ErrorLevelEnum, LogToEnum

class Logger():
    __metaclass__ = Singleton
    
    __LOG_FILE_NAME = "/home/pi/Desktop/PeepNee/sample/errorLog.txt"
    
    def __init__(self):
        self.configuration = GlobalConfigurationWrapper()
        self.minimalLogLevel = ErrorLevelEnum[self.configuration.logging_log_level()]
        self.logTo = LogToEnum[self.configuration.logging_log_to()]

    def log_information(self, message):
        if(self.minimalLogLevel <= ErrorLevelEnum.Information):
            self.__write('INFO: ' + message)
            
    def log_error(self, message):
        if(self.minimalLogLevel <= ErrorLevelEnum.Error):        
            self.__write('ERROR: ' + message)
            
    def log_critical(self, message):
        if(self.minimalLogLevel <= ErrorLevelEnum.Critical):
            self.__write('CRITICAL: ' + message)
            #TODO: Send email if configured
    
    def __write(self, message):
        logType = self.logTo 
        
        if(logType == LogToEnum.Console):
            print(message)

        elif(logType == LogToEnum.File):
            f = open(self.__LOG_FILE_NAME, "a")
            f.write(message + '\n')
            f.flush()
            f.close()
      
# Usage example
# logger = Logger()
# logger.log_critical('<imageUploadManager.uploadImage>')

