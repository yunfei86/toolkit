"""
This module provides convenient methods to run shell commands and get the status and return values.
"""
import sys

from logbase    import LogBase
from re         import search
from subprocess import Popen, PIPE

class IonSystem(object):
    logBase = LogBase('IonSystem')
    logBase.createRotatingFileLogger('log/ionunittest.log')
    logger = logBase.logger
       
    def __init__(self):
        self.popen     = None
        self.stdoutput = None
        """@ivar: This varialbe stores the output from the C{stdout}"""
        self.stderror  = None
        """@ivar: This varialbe stores the output from the C{stderr}"""
        self.cmd       = 'Not Set'

    def execute(self, cmd, shellFlag = False, ioFlag = False):
        """
        This method executes a command passed through the argument.
        @type cmd: string
        @param cmd: The command to be executed.
        @rtype: void
        @return: None.
        """
        if self.cmd == None or self.cmd == '':
            self.logger.warn('Command was empyty or None!')
            return
        self.cmd = cmd
        self.stdoutput = None
        self.stderror  = None
        self.logger.info('Executing command: %s'%cmd)
        if search("\|", cmd) != None:
            self.logger.error('The command [%s] can not pipe to other process.'%cmd)
            raise Exception('Command [%s] can not use pipe!'%cmd)
        self.logger.debug('cmd.split(' '): %s'%cmd.split(' '))
        inputPipe = None
        if ioFlag:
            inputPipe = PIPE
        self.popen = Popen(cmd.split(' '), stdin=inputPipe, stdout=PIPE, stderr=PIPE, shell=shellFlag)
        returnValue = self.popen.communicate()
        if returnValue[0]:
            self.stdoutput = returnValue[0].strip()
        else: self.stdoutput = returnValue[0]
        if returnValue[1]:
            self.stderror  = returnValue[1].strip()
        else: self.stderror  = returnValue[1]
        self.logger.debug('Std Out'.center(80,'-'))
        self.logger.debug('%s'%returnValue[0])
        self.logger.debug('Done'.center(80,'.'))
        self.logger.debug('Std Err'.center(80,'-'))
        self.logger.debug('%s'%returnValue[1])
        self.logger.debug('Done'.center(80,'.'))
        #if not self.noError():
        #    raise Exception('Command: [%s] caused the error: [%s]'%(cmd, self.stderror))
        
    def getCmd(self):
        """
        A convenience method to recollect the command previously executed.
        @rtype: string
        @return: The command executed previously.
        """
        return self.cmd
    
    def noError(self):
        """
        A convenience method to check the error status of the command previously executed.
        @rtype: boolean
        @return: The the status of the command executed previously.
        """
        return self.stderror == ''
    
    def getStdOut(self):
        """
        A convenience method to get the output of the command previously executed.
        @rtype: string
        @return: The return value of the command executed.
        """
        return self.stdoutput
    
    def getStdErr(self):
        """
        A convenience method to get the error of the command previously executed.
        @rtype: string
        @return: The error value of the command executed.
        """
        return self.stderror
        