import os, sys
import urllib, urllib2, ConfigParser
from  cookielib import CookieJar
from   time     import strftime, sleep
from  threading import Thread
from   quearydb import IonDB
from         re import search
from  ionsystem import IonSystem

from logbase import LogBase
class ProtonAnalysis(LogBase):
    """
    This class provides methods to launch a Proton/PGM run on a remote host.
    @author: Ranjan Muthumalai

        Usage:
        
        >>> from proton_batch import ProtonAnalysis
        >>> pa1 = ProtonAnalysis('sirius.itw', 'SP5-13',os.path.join(fileDir, 'startanalysis-ebr-rdat-sirius.cfg'),
                                 os.path.join(fileDir, 'SP5ebr.txt'),wait=False,debug=True)

    """
    def __init__(self, host, expName, configFileName, rptNameFile, wait=False, fromStage='fromRaw', debug=False):
        """
        @type  host: string
        @param host: Host Torrent Server on which the user wants to launch an analysis. This could be a
                     valid name like 'borabora.itw' or an IP address
        @type  expName: string
        @param expName: Part of the experiment name from which the run could be searched from the Torrent Server
        @type configFileName: string
        @param configFileName: This is the name of the config file which contains many information about the analysis
                                parameters
        @type rptNameFile: string
        @param rptNameFile: This is a text file which is used to save the report name of the current run. This will be
                            used in the runs from base calling
        @type wait: boolean
        @param wait: This boolean indicates wether the current run has to wait until a paritcular run is complete. This
                        is an optional parameter with default value Fasle.
        @type fromStage: string
        @param fromStage: This parameter can take two values: 1) 'fromRaw' and 2) 'fromWells' indicating if the user
                            would like the run to be from raw data or from base calling. This is an optional parameter
                            with default value 'fromRaw'
        @type debug: boolean
        @param debug: This boolean indicates if the user wants the debug messages to be printed during the execution.
                        The default value of the parameter is False
        """
        super(ProtonAnalysis, self).__init__('ProtonAnalysis', 'debug')
        self.createRotatingFileLogger('log/ionunittest.log')
        if debug:
            self.logger.setLevel('DEBUG')
        else:
            self.logger.setLevel('INFO')
        self.logger.debug('Proton analysis is starting in [%s]'%os.getcwd())
        self.host    = host
        self.expName = expName
        self.debug   = debug
        self.rptNameFile = rptNameFile
        self.wait        = wait
        self.fromStage  = fromStage
        self.system = IonSystem()
        if(not os.path.exists(configFileName)):
            raise Exception('Config File: [%s] does not exist!'%configFileName)
        self.config  = ConfigParser.ConfigParser()
        self.__loadConfigFile(configFileName)
        if not self.chiptype:
            raise Exception('No Chip type informatin is given in the config file [%s]'%configFileName)
        self.dbArgs = self.__getArguments(self.chiptype)
        for l in self.dbArgs:
            self.logger.info('Db Args: %s'%l)
        t = Thread(target = self.start, name = '%s_thread'%expName)
        #t.daemon = True
        t.start()
        t.join()
        #self.start()

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

    def __getIdAndPath(self, runName):
        """
        This is a private method to get the ID and the path of the expriment directory.
        @type runName: string
        @param runName: Run name.
        """
        idb = IonDB(self.host, True)
        idb.queary("""select id,"expDir" from rundb_experiment where "expDir" like '%s'"""%runName)
        if len(idb.rows) == 1:
            return idb.rows[0]
        elif len(idb.rows) == 0:
            self.logger.warn('Could not get Id and Path for [%s]'%runName)
            return None
        else:
            self.logger.warn("The queary returned multiple rows!")
            self.logger.warn('='*80)
            for row in idb.rows:
                self.logger.warn('Row: %s'%row)
            self.logger.warn("Done.")
        return None

    def __getPreviousReport(self, rptName):
        """
        This is a private method to get the previous report name. This is used to run from base calling.
        @type rptName: string
        @param rptName: This is the previous report name from which the 1.wells file will be used
        """
        idb = IonDB(self.host, True)
        idb.queary("""SELECT "reportLink" from rundb_results where "reportLink" like '%%%s%%'"""%rptName)
        if (len(idb.rows) == 1):
            return idb.rows[0][0]
        else:
            self.logger.debug('Length of queary result: %s'%len(idb.rows))
            for row in idb.rows:
                self.logger.debug('Row: %s'%row[0])
                if not search('from', row[0]):
                    return row[0]
            raise Exception('The queary did not return the correct report link!')

    def __getAnalysisSvnNo(self):
        """
        This is a private method to get the svn number of the Analysis binary.
        """
        hostAvailable = self.__ping(self.host)
        if not hostAvailable:
            sleep(60)
            hostAvailable = self.__ping(self.host)
            if not hostAvailable:
                self.logger.warn('Host [%s] did not respond even after a 60sec wait!'%self.host)
        if hostAvailable:
            #self.system.execute("ssh root@%s Analysis|grep Version|awk '{print $4}'"%self.host)
            self.system.execute("ssh ionadmin@%s Analysis"%self.host)
            if self.system.getStdErr() == '':
                reply = self.system.getStdOut()
                self.logger.debug('Reply from command: %s'%reply)
                replyList = reply.split("\n")
                for line in replyList:
                    if(search('Version', line)):
                        lineList = line.split(" ")
                        svnNo = lineList[-2].strip()
                #raise Exception('Stop: %'%reply1)
                self.logger.info('Return value: %s'%svnNo)
                return svnNo[1:-1]
            else:
                return 'Err'
        else:
            self.logger.warn('Could not ping host [%s] and did not start analysis'%self.host)
            return 'NoHost'

    def __getArguments(self, chipID):
        """
        This is a private method to get the default arguments of the beadFind, Analysis and Basecaller.
        @type chipID: string
        @param chipID: Chip id like 314, 316, 318 or 900.
        """
        idb = IonDB(self.host, True)
        if self.thumbnail:
            idb.queary("""SELECT thumbnailbeadfindargs, thumbnailanalysisargs, thumbnailbasecallerargs  from rundb_chip where name =  '%s'"""%chipID)
        else:
            idb.queary("""SELECT beadfindargs, analysisargs,basecallerargs from rundb_chip where name =  '%s'"""%chipID)
        if (len(idb.rows) == 1):
            return idb.rows[0]
        else:
            self.logger.debug('Length of queary result: %s'%len(idb.rows))
            for row in idb.rows:
                self.logger.debug('Row: %s'%row[0])
                if not search('from', row[0]):
                    return row[0]
            raise Exception('The queary did not return the correct report link!')

    def __loadConfigFile(self, configFileName):
        """
        This is a private method to get the contents of the configuration file.
        @type configFileName: string
        @param configFileName: The name of the configuration file.
        """
        if os.path.exists(configFileName):
            try:
                self.config.read(configFileName)
                self.__readSection('General')
                if self.thumbnail:
                    self.__readSection('ThumbnailAnalysis')
                else:
                    self.__readSection('FullChipAnalysis')
            except:
                print 'Exception [%s]: %s'%(sys.exc_info()[0].__name__, sys.exc_info()[1])

    def __readReportName(self, rptFileName):
        """
        This is a private method to get the contents of the report file.
        @type rptFileName: string
        @param rptFileName: The name of the report file.
        """
        if os.path.exists(rptFileName):
            try:
                f = open(rptFileName, 'r')
                name = f.readline().strip()
                if name == '':
                    raise Exception('Got an empty line from file [%s]'%rptFileName)
                return name
            except:
                print 'Exception [%s]: %s'%(sys.exc_info()[0].__name__, sys.exc_info()[1])
        else:
            raise Exception('File [%s] contaning the previous report name does not exist!'%rptFileName)

    def __readSection(self, sectionName):
        """
        This is a private method to get the contents of a section from the configuration file.
        @type sectionName: string
        @param sectionName: The name of the section in file.
        """
        if self.config.has_section(sectionName):
            for k, v in self.config.items(sectionName):
                self.logger.debug('%s = %s.'%(k, v))
                self.__setattr__(k, self.__value(v))

    def __value(self, valueStr):
        """
        This is a private method to get the value from the string.
        @type valueStr: string
        @param valueStr: The value read from the config file.
        """
        try:
            return int(valueStr)
        except:
            try:
                return float(valueStr)
            except:
                if (valueStr.lower() == 'true'):
                    return True
                if (valueStr.lower() == 'false'):
                    return False
                if (valueStr.lower() == 'none'):
                    return None
                if ((valueStr[0] == '[') and (valueStr[-1] == ']')):
                    tmpStr = str.strip(valueStr[1:-2])
                    self.logger.debug('tmpStr: %s'%tmpStr)
                    tmpList = tmpStr.split(',')
                    return [str.strip(i) for i in tmpList]
                return valueStr

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

    def __isComplete(self, runName):
        status = self.__getAnalysisStatus(runName)
        if status != None:
            return status == 'Completed'
        else:
            return False

    def __setGPUValue(self, analysisArg):
        if not analysisArg:
            self.logger.debug("Analysis Argument is None. Adding from DB [%s]"%self.dbArgs[1])
            analysisArg = self.dbArgs[1]
        else:
            self.logger.debug("Analysis Argument is not None.")
        self.logger.debug("Analysis Argument is [%s]"%analysisArg)
        if analysisArg.find('gpuWorkLoad') == -1:
            analysisArg = '%s --%s'%(analysisArg, 'gpuWorkLoad 0')
            self.logger.debug("No gpuWorkLoad found in the argument. Added one.")
            self.logger.debug("Analysis Argument after adding the gpu flag is [%s]"%analysisArg)
        if self.gpuflag:
            self.logger.debug("GPU flag is True. Will switch on gpuWrokLoad")
            if analysisArg.find('gpuWorkLoad 0') > -1:
                analysisArg = analysisArg.replace('gpuWorkLoad 0', 'gpuWorkLoad 1')
        else:
            self.logger.debug("GPU flag is False. Will switch off gpuWrokLoad")
            if analysisArg.find('gpuWorkLoad 1') > -1:
                analysisArg = analysisArg.replace('gpuWorkLoad 1', 'gpuWorkLoad 0')

        return analysisArg

    def __getCurArg(self):
        moreValues = {}
        argStuffList = [self.beadfindargs, self.analysisargs, self.basecallerargs]
        for i in range(3):
            if argStuffList[i]:
                moreValues[self.arglist[i]] = argStuffList[i]
        
        if hasattr(self, 'gpuflag'):
            self.logger.debug("GPU flag is available")
            if not moreValues.has_key(self.arglist[1]):
                moreValues[self.arglist[1]] = None
            moreValues[self.arglist[1]] = self.__setGPUValue(moreValues[self.arglist[1]])
        else:
            self.logger.debug("GPU flag is not available")
            #The argument is not changed if gpuflag is not given

        #if (self.sdat):
        #    tmpCmd = self.dbArgs[1]
        #    if(self.thumbnail and self.analysisargs == None):
        #        moreValues[self.arglist[1]] = '/results/csugnet/runSdatAnalysis100x100.pl %s'%tmpCmd[8:]
        #    if(self.thumbnail == False and self.analysisargs == None):
        #        moreValues[self.arglist[1]] = '/results/csugnet/runSdatAnalysis224x216.pl %s'%tmpCmd[8:]

        return moreValues

    def start(self):
        expId, expDir = self.__getIdAndPath('%%%s%%'%self.expName)
        if self.baserecal:
            ebrString = 'ebr'
        else:
            ebrString = 'noebr'
        if self.sdat:
            sdatStr = 'sdat'
        else:
            sdatStr = 'rdat'

        if self.addsvn:
            self.prefix = '%s-%s-'%(self.prefix,self.__getAnalysisSvnNo())
        if self.thumbnail:
            reportName = '%s%s-tn-%s-%s_%s'%(self.prefix, self.expName, sdatStr, strftime('%m%d-%H%M%S'), ebrString)
        else:
            reportName = '%s%s-fc-%s-%s_%s'%(self.prefix, self.expName, sdatStr, strftime('%m%d-%H%M%S'), ebrString)

        moreValues = self.__getCurArg()

        if self.wait:
            reportName = '%s-%s'%(reportName, self.fromStage)
            waitResultName = self.__readReportName(self.rptNameFile)
            self.logger.debug('resultprefix: %s'%self.resultprefix)
            
            self.logger.info('Will wait for the run [%s] to complete'%waitResultName)
            while self.__getAnalysisStatus(waitResultName) not in ['Base Calling', 'Alignment', 'Completed']:
                self.logger.debug('Waiting for two min for run [%s] to complete'%waitResultName)
                sleep(120)
                
            # wait for 1 more minutes
            sleep(20)
            fullPath = self.__getPreviousReport(waitResultName)
            moreValues['previousReport'] = os.path.join(self.resultprefix, fullPath[1:-1])
            moreValues['previousThumbReport'] = os.path.join(self.resultprefix, fullPath[1:-1])
            self.logger.debug('previousReport: %s'%moreValues['previousReport'])
            #while not self.__isComplete(waitResultName):
            #    self.logger.debug('Waiting for two min for run [%s] to complete'%waitResultName)
            #    sleep(120)
        else:
            self.logger.debug('Writing [%s] to file [%s]'%(reportName, self.rptNameFile))
            f = open(self.rptNameFile, 'w')
            f.write('%s\n'%reportName)
            f.close()
        for k in moreValues.keys():
            self.logger.debug('moreValues: key[%s] = value[%s]'%(k, moreValues[k]))   
        self.logger.info('Preparing to launch the run [%s]'%reportName)
        paramsDict = {'report_name'    :reportName,
                        'path'         :expDir,
                        'blockArgs'    :self.fromStage
                        }
        if(self.baserecal):
            paramsDict['do_base_recal'] = self.baserecal
        if(self.thumbnail):
            paramsDict['do_thumbnail'] = self.thumbnail
        if(moreValues != {}):
            paramsDict.update(moreValues)
        params = urllib.urlencode(paramsDict)
        for k in paramsDict.keys():
            self.logger.debug('paramsDict: key[%s] = value[%s]'%(k, paramsDict[k]))

        theUrl = 'http://%s/report/analyze/%s/0/'%(self.host, expId)
        loginUrl = "http://%s/login/ajax/"%self.host
        self.logger.debug('The URL [%s]'%theUrl)
        self.logger.debug('Login URL [%s]'%loginUrl)
        self.logger.debug('Params: %s'%params)

        cookieJar = CookieJar()
        opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cookieJar),
                                      urllib2.HTTPHandler(debuglevel=2))
 
        # ===========================================================
        # Get csrftoken from login page - needed while login is csrf protected
        #csrftoken = None
        #try:
        #    response = opener.open(loginUrl) ## GET
        #
        #    for c in cookieJar:
        #        if c.name == 'csrftoken':
        #            csrftoken = c.value
        #            self.logger.info("SUCCESS: Got CSRF from cookie '%s'", csrftoken)
        #            break
        #        else:
        #            self.logger.error("Failed to get CSRF Token")
        #
        #except urllib2.HTTPError as e:
        #    self.logger.exception("Fetch CSRF failed: %d", e.code)
        #
        # Authentication information
        auth = {'username': 'ionadmin', 'password': 'ionadmin'}
        #if csrftoken:
        #    auth.update({'csrfmiddlewaretoken': csrftoken})
        # ============================================================
        # Post to /login/ with username, password (and csrf token while # required)
        try:
            request = urllib2.Request("http://%s/login/" % self.host, data=urllib.urlencode(auth))
            response = opener.open(request)
            #cookieJar.extract_cookies(response,request)
            self.logger.info("Login Session Successful")
            #request = urllib2.Request("http://%s/login/" % self.host, data=urllib.urlencode(auth))
            response = opener.open(theUrl, params)
        except urllib2.HTTPError as e:
            self.logger.exception("Auth /login/ Failed: %d", e.message)

        self.logger.info('Done launching the analysis [%s]'%reportName)
        self.logger.info('===============================================================')
        return reportName
