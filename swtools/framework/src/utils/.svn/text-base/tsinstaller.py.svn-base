from logbase         import LogBase
from ionsystem       import IonSystem
from sshcmd          import SshCmd
from re              import search

class TSInstaller(object):
    logBase = LogBase('TSInstaller')
    logBase.createRotatingFileLogger('log/ionunittest.log')
    logger  = logBase.logger
    cmd = { 'updateSourceList'   : '/etc/apt',
            'copySourceList'     : '/etc/apt/sources.list',
            'update'             : 'apt-get --quiet update',
            'installConfig'      : 'apt-get --quiet --assume-yes --force-yes install ion-tsconfig',
            'runtsconfig'        : 'TSconfig --update-torrent-suite',
            'installrndplugin'   : 'apt-get --quiet --assume-yes --force-yes install ion-rndplugins',
            'dpkg'               : 'dpkg -l ion-*',
            'greptsconfigError'  : 'grep -i error /var/log/ion/tsconfig_install.log',
            'gettsconfigStatus'  : 'grep "TSconfig software update" /var/log/ion/tsconfig_install.log'}
    def __init__(self, hostName):
        self.hostname = hostName
        self.logger.debug('Host name is [%s]'%self.hostname)
        self.sshcmd = SshCmd('root', self.hostname)
        self.hostAvailable = self.__ping(self.hostname)
        self.logger.debug('Host [%s] is available [%s]'%(self.hostname, self.hostAvailable))

    def __ping(self, hostname):
        system = IonSystem()
        system.execute('ping -c 2 %s'%hostname)
        op = system.getStdOut()
        self.logger.debug(op)
        opList =filter(lambda x: search("%", x), op.split())
        if len(opList) != 1:
            return False
        return float(opList[0][:-1]) == 0

    def __createLocalSourceList(self, source, level, newSourceList):
        origFile = open('src/utils/sources.list.orig', 'r')
        sourceFile = open(newSourceList, 'w')
        for line in origFile:
            sourceFile.write(line)
        sourceFile.write('%s %s/\n'%(source, level))
        origFile.close()
        sourceFile.close()
        self.logger.debug('Created source list at: %s'%newSourceList)
        
    def updateSourceList(self, source, level, target):
        if not self.hostAvailable:
            self.logger.error('Host [%s] is not reachable!'%self.hostname)
            return 'fail'
        self.logger.debug('The source list: %s'%target)
        self.logger.debug('The Source: %s'%source)
        self.logger.debug('The level to update is [%s]'%level)
        self.__createLocalSourceList(source, level, target)
        #self.system.execute(self.cmd['updateSourceList']%(target, self.hostname))
        self.sshcmd.scpTo(target, self.cmd['updateSourceList'])
        return self.sshcmd.getStdErr()
        
    def copySourceList(self, targetDir):
        if not self.hostAvailable:
            self.logger.error('Host [%s] is not reachable!'%self.hostname)
            return 'fail'
        self.logger.debug('The target directory: %s'%targetDir)
        #self.system.execute(self.cmd['copySourceList']%(self.hostname,target))
        self.sshcmd.scpFrom(self.cmd['copySourceList'], targetDir)
        return self.sshcmd.getStdErr()
        
    def update(self):
        if not self.hostAvailable:
            self.logger.error('Host [%s] is not reachable!'%self.hostname)
            return 'fail'
        #self.system.execute(self.cmd['update']%self.hostname)
        self.sshcmd.ssh(self.cmd['update'])
        return self.sshcmd.getStdErr()

    def updateTsConfig(self):
        if not self.hostAvailable:
            self.logger.error('Host [%s] is not reachable!'%self.hostname)
            return 'fail'
        #self.system.execute(self.cmd['installConfig']%self.hostname)
        self.sshcmd.ssh(self.cmd['installConfig'])
        return self.sshcmd.getStdErr()

    def getTsConfigStatus(self):
        if not self.hostAvailable:
            self.logger.error('Host [%s] is not reachable!'%self.hostname)
            return
        #self.system.execute(self.cmd['tsconfigError']%self.hostname)
        self.sshcmd.ssh(self.cmd['greptsconfigError'])
        return self.sshcmd.getStdOut()

    def getInstallStatus(self):
        if not self.hostAvailable:
            self.logger.error('Host [%s] is not reachable!'%self.hostname)
            return
        #self.system.execute(self.cmd['gettsconfigStatus']%self.hostname)
        self.sshcmd.ssh(self.cmd['gettsconfigStatus'])
        return self.sshcmd.getStdOut() == 'TSconfig software update process completed successfully'

    def installTsConfig(self):
        if not self.hostAvailable:
            self.logger.error('Host [%s] is not reachable!'%self.hostname)
            return 'fail'
        #self.system.execute(self.cmd['runtsconfig']%self.hostname)
        self.sshcmd.ssh(self.cmd['runtsconfig'])
        return self.sshcmd.getStdErr()

    def installRndPlugins(self):
        if not self.hostAvailable:
            self.logger.error('Host [%s] is not reachable!'%self.hostname)
            return 'fail'
        #self.system.execute(self.cmd['runtsconfig']%self.hostname)
        self.sshcmd.ssh(self.cmd['installrndplugin'])
        return self.sshcmd.getStdErr()

    def getSWVersion(self):
        if not self.hostAvailable:
            self.logger.error('Host [%s] is not reachable!'%self.hostname)
            return ''
        #self.system.execute(self.cmd['dpkg']%self.hostname)
        self.sshcmd.ssh(self.cmd['dpkg'])
        return self.sshcmd.getStdOut()
