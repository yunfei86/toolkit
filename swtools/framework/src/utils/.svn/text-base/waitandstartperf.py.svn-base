import os, sys, glob

from       time import strftime, sleep
from         re import search
from   quearydb import IonDB
from  ionsystem import IonSystem
from    logbase import LogBase

class WaitAndStartPerf(object):
    logBase = LogBase('WaitAndStartPerf','debug')
    logBase.createRotatingFileLogger('log/ionunittest.log', level='debug')
    logger  = logBase.logger 
    def __init__(self, host, svnTag, perfHome, initialWait=40):   
        self.system = IonSystem()
        if not svnTag:
            raise Exception('The SVN Tag is None!')
        if not self.__ping(host):
            raise Exception('Ping failed for host [%s]!'%host)
        self.__checkForExistance(perfHome)
        self.__checkForExistance(os.path.join(perfHome, 'precomp.php'))
        self.__checkForExistance(os.path.join(perfHome, 'lists'))
        self.__checkForExistance(os.path.join(perfHome, 'mklocal.sh'))
        self.__checkForExistance(os.path.join(perfHome, 'upload.sh'))
        self.logger.info('All the files from the directory [%s] are available'%perfHome)
            
        self.host = host
        self.svnTag = svnTag
        self.initialWait = initialWait * 60
        self.logger.debug('Host is [%s]'%self.host)
        self.logger.debug('SVN Tag is [%s]'%self.svnTag)
        self.logger.debug('Initial wait is [%s] Min'%(self.initialWait/60))
        listFiles = glob.glob(os.path.join(perfHome, 'lists', 'SP5-13-sirius.list.*'))
        numList = []
        for elem in listFiles:
            temp = elem.split('list.')
            numList.append(int(temp[1]))
        numList.sort()
        newNum = numList[-1] + 1
        self.logger.debug('The new list extension is [%s]'%newNum)
        self.runList = []
        self.__getReportList()
        sleep(self.initialWait)
        self.__waitForRunsFinish()
        os.chdir(perfHome)
        self.logger.debug('The current dir [%s]'%os.getcwd())
        self.system.execute('php precomp.php -h %s -f dataset.txt -q 4 -s %s -l lists'%(self.host, self.svnTag))
        sleep(2)
        self.logger.debug('The current dir [%s]'%os.getcwd())
        self.system.execute('php index.php -h %s -s -sirius.list -x %s -f dataset.txt'%(self.host, newNum))
        f = open(os.path.join(perfHome, 'index.html'), 'w')
        f.write('%s\n'%self.system.getStdOut())
        f.flush()
        f.close()
        sleep(2)
        self.system.execute('ssh ionadmin@sirius.itw mkdir /home/ionadmin/anacomp/%s'%svnTag)
        sleep(2)
        self.system.execute('scp -r csss plots index.html ionadmin@sirius.itw:/home/ionadmin/anacomp/%s'%svnTag)
        sleep(2)
        self.system.execute('scp mknewlink.sh ionadmin@sirius.itw:/home/ionadmin/anacomp')
        sleep(2)
        self.system.execute('ssh ionadmin@sirius.itw /home/ionadmin/anacomp/mknewlink.sh')
        
    def __checkForExistance(self, filePath):
        if not os.path.exists(filePath):
            self.logger.error('[%s] dose not exist!'%filePath)
            raise Exception('[%s] dose not exist!'%filePath)
        
    def __waitForRunsFinish(self):
        allWaitStatus = False
        while not allWaitStatus:
            for run in self.runList:
                runStatus = self.__getAnalysisStatus(run)
                allWaitStatus = allWaitStatus or (runStatus == 'Completed')
                print 'Run [%s] has a status [%s]'%(run, runStatus)
                self.logger.debug('Run [%s] has a status [%s]'%(run, runStatus))
            sleep(120)
            
    def __getReportList(self):
        idb = IonDB(self.host)
        idb.queary("SELECT \"resultsName\" FROM  public.rundb_results where \"resultsName\" like '%%%s%%' ORDER BY rundb_results.\"timeStamp\""%self.svnTag)
        for row in idb.rows:
            self.runList.append(row[0])
            print self.runList
        
    def __ping(self, hostname):
        """
        This is a private method and used to ping a host and detect its existance.
        @type hostname: string
        @param hostname: This the name of the host or an IP address
        """
        self.system.execute('ping -c 2 %s'%hostname)
        op = self.system.getStdOut()
        self.system.logger.debug(op)
        opList =filter(lambda x: search("%", x), op.split())
        if len(opList) != 1:
            raise Exception('More than 1 % got from ping result [%s]'%op)
        return float(opList[0][:-1]) == 0
    
    def __getAnalysisStatus(self, runName):
        """
        This is a private method to get the current status of the run.
        @type runName: string
        @param runName: The name of the run.
        """
        idb = IonDB(self.host)
        idb.queary("""SELECT status FROM  public.rundb_results where \"resultsName\" like '%s'"""%runName)
        if len(idb.rows) == 1:
            return idb.rows[0][0]
        else:
            self.logger.warn('The queary has [%s] rows'%len(idb.rows))
            self.logger.warn('The rows: %s'%idb.rows)
        return None