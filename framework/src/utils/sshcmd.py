"""
This module runs ssh and scp.
"""
from ionsystem import IonSystem

class SshCmd(IonSystem):
    """
    SshCmd is a convenient class helps to run ssh and scp. It inherits IonSystem and wraps the commands with
    ssh and scp commands.
    """
    def __init__(self, user, hostName):
        """
        @type user: string
        @param user: The user in the ssh command
        @type hostName: string
        @param hostName: The host on wich the ssh command is executed
        """
        super(SshCmd, self).__init__()
        self.__user = user
        self.__hostName = hostName
        self.logger.debug('The user: %s'%self.__user)
        self.logger.debug('The host: %s'%self.__hostName)
        self.__sshString = ' '.join(['ssh %s@%s'%(self.__user, self.__hostName), '%s'])
        self.__scpFromString = 'scp %s@%s:'%(self.__user, self.__hostName)
        
    def ssh(self, cmd, ioFlag = False):
        """
        This method executes the ssh command.
        @type cmd: string
        @param cmd: The command to be executed.
        @type ioFlag: boolean
        @param ioFlag: This flag sets the interaction with the Popen
        @rtype: void
        @return: None.
        """
        self.execute(self.__sshString%cmd, ioFlag = ioFlag)

    def scpFrom(self, sourceFile, targetDir):
        """
        This method scp source file from a remote host to the target directory.
        @type sourceFile: string
        @param sourceFile: The source file not directory (full path)
        @type targetDir: string
        @param targetDir: The target file/dir (full path)
        @rtype: void
        @return: None.
        """
        self.execute('%s%s %s'%(self.__scpFromString, sourceFile, targetDir))
        
    def scpTo(self, sourceFile, targetDir):
        """
        This method scp source file to a remote host's target directory.
        @type sourceFile: string
        @param sourceFile: The source file not directory(full path)
        @type targetDir: string
        @param targetDir: The target file/dir (full path)
        @rtype: void
        @return: None.
        """
        self.execute('scp %s %s@%s:%s'%(sourceFile, self.__user, self.__hostName, targetDir))
        
