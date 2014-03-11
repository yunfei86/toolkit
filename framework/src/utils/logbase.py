"""
This class provides a wrapper to make logger which will log messages on screen, in a file,
in a rotating file.
"""
import os, sys, logging, logging.handlers

class LogBase(object):
    """
    This class provides a wrapper to make logger which will log messages on screen, in a file,
    in a rotating file.
    """
    levelStrList = ['NOTSET', 'DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL']
    levels       = {'NOTSET':logging.NOTSET,   'DEBUG':logging.DEBUG, 'INFO':logging.INFO,
                    'WARNING':logging.WARNING, 'ERROR':logging.ERROR, 'CRITICAL':logging.CRITICAL}
    rootName = 'LogRoot'
    def __init__(self, logName, level='INFO'):
        """
        Constructor takes two parameters.
        @type  logName: string
        @param logName: This gives a name to the logger
        @type    level: string
        @param   level: This indicates one of the log levels ['NOTSET', 'DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL']
        """
        self.loggerName = logName
        self.logger     = logging.getLogger('%s.%s'%(self.rootName,self.loggerName))
        #self.logger.propagate = False
        self.logger.setLevel(logging.DEBUG)
        self.complexFormat = '%(asctime)s - %(name)s - %(levelname)8s - %(module)s[%(lineno)5d]: - %(message)s'
        self.simpleFormat  = '%(asctime)s - %(name)22s - %(levelname)8s - %(message)s'
        #self.simpleFormat  = '%(name)s - %(levelname)8s - %(module)s - %(message)s'
        self.createConsoleLogger(level)
    
    def __getLevel(self, level):
        """
        This is a private method which converts a string of a loglevl to logging level object.
        @type  level: string
        @param level: This is one of the levels in string format
        @rtype: integer
        @return: logging level from python module U{B{logging}<http://docs.python.org/2/library/logging.html#module-logging>}
        """
        if level == None: return logging.DEBUG
        levelUpper = level.upper()
        if levelUpper in self.levelStrList:
            return self.levels[levelUpper]
        else: return logging.DEBUG

    def __checkLogDir(self, logDir):
        """
        This is a private method which checks the availability of log file directory.
        @type  logDir: string
        @param logDir: This is a directory where the log files will be saved.
        @rtype: boolean
        @return: A boolean of weather the directory exists or not.
        """
        #if not os.path.exists(os.path.dirname(logDir)):
        #    raise Exception('Log dir [%s] does not exist!'%os.path.dirname(logDir))
        dirName = os.path.dirname(logDir)
        if not os.path.exists(dirName):
            try:
                os.makedirs(dirName)
            except:
                self.logger.exception(sys.exc_info)
                return False
        return os.path.exists(dirName)
    
    def createFileLogger(self, fileName, level, formatString=None):
        """
        This method creates a log file.
        @type  fileName: string
        @param fileName: This is the file where the logs will be written.
        @type  level: string
        @param level: This is one of the levels in string format
        @type  formatString: string
        @param formatString: This is the format of the log being written
        @rtype: void
        @return: None.
        """
        if self.__checkLogDir(fileName):
            if not formatString:
                formatString = self.complexFormat
            handler = logging.FileHandler(fileName, mode='a', encoding=None, delay=False)
            handler.setLevel(self.__getLevel(level))
            handler.setFormatter(logging.Formatter(formatString))
            self.logger.addHandler(handler)
        else: self.logger.warn('The log file [%s] is not created as the directory [%s] is not existing!'%
                               (fileName, os.path.dirname(fileName)))

    def createRotatingFileLogger(self, fileName, level='debug', maxbytes=20480, backupCount=5, formatString=None):
        """
        This method creates rotating log files.
        @type  fileName: string
        @param fileName: This is the file where the logs will be written.
        @type  level: string
        @param level: This is one of the levels in string format
        @type maxbytes: integer
        @param maxbytes: This is the size of the rotating log file
        @type backupCount: integer
        @param backupCount: This is the number of rotating logs that would be maintained
        @type  formatString: string
        @param formatString: This is the format of the log being written
        @rtype: void
        @return: None.
        """
        if self.__checkLogDir(fileName):
            if not formatString:
                formatString = self.complexFormat
            handler = logging.handlers.RotatingFileHandler(fileName, mode='a', maxBytes=maxbytes, backupCount=backupCount, encoding=None, delay=0)
            handler.setLevel(self.__getLevel(level))
            handler.doRollover()
            handler.setFormatter(logging.Formatter(formatString))
            self.logger.addHandler(handler)
        else: self.logger.warn('The log file [%s] is not created as the directory [%s] is not existing!'%
                               (fileName, os.path.dirname(fileName)))
        
    def createConsoleLogger(self, level, formatString=None):
        """
        This method logs messages in the console.
        @type  level: string
        @param level: This is one of the levels in string format
        @type  formatString: string
        @param formatString: This is the format of the log being written
        @rtype: void
        @return: None.
        """
        if not formatString:
            formatString = self.simpleFormat
        handler = logging.StreamHandler()
        handler.setLevel(self.__getLevel(level))
        handler.setFormatter(logging.Formatter(formatString))
        self.logger.addHandler(handler)