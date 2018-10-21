from configurationWrapping import GlobalConfigurationWrapper
from patternImplementations import Singleton
from enums import ErrorLevelEnum, LogToEnum

class Logger():
    __metaclass__ = Singleton
    
    def __init__(self):
        self.configuration = GlobalConfigurationWrapper()
        self.logLevel = ErrorLevelEnum[self.configuration.logging_log_level()]
        self.logTo = LogToEnum[self.configuration.logging_log_to()]

    def log_information(self, message):
        if(self.logLevel <= ErrorLevelEnum.Information):
            self.__write(message)
            
    def log_error(self, message):
        if(self.logLevel <= ErrorLevelEnum.Error):        
            self.__write(message)
            #TODO: Send email if configured
            
    def log_critical(self, message):
        if(self.logLevel <= ErrorLevelEnum.Critical):
            self.__write(message)
            #TODO: Send email if configured
    
    def __write(self, message):
        logType = self.logTo
        
        if(logType == LogToEnum.Console):{
                print(message)
            }
        elif(logType == LogToEnum.File):{
                #TODO: Implement writing to a file as rolling appender
            }
      


