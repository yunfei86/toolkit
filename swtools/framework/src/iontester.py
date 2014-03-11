import ConfigParser
import os, sys, argparse, inspect, types, shutil

import ionunittest
from ionunittest.signals import installHandler
from filelock            import FileLock
from threading           import Thread
from time                import sleep, strftime

verNum = float(sys.version.split()[0][:-2])

if 2.4 <= verNum <= 2.6:
    import unittest2 as unittest
else:
    import unittest

from logbase import LogBase

class IonTester(LogBase):
    logLevel=['DEBUG', 'INFO', 'WARN']
    def __init__(self, testRoot, testListFile=None, consoleLogLevel='info', reportName=None, outputDir='results', catchBreak=False, failfast=False, buffer=False, exit=True):
        super(IonTester, self).__init__('IonTester', consoleLogLevel)
        self.createRotatingFileLogger('log/ionunittest.log', consoleLogLevel)
        self.testRunner = ionunittest.runner.HtmlTestRunner
        self.testLoader = ionunittest.TestLoader()
        if not reportName:
            reportName = 'Ion Test Report'
        self.logger.debug('The test root directory: %s'%testRoot)
        self.logger.debug('The test list file     : %s'%testListFile)
        self.logger.debug('The console log level  : %s'%consoleLogLevel)
        self.logger.debug('The output directory   : %s'%outputDir)
        self.logger.debug('The catch Break        : %s'%catchBreak)
        self.logger.debug('The failfast           : %s'%failfast)
        self.logger.debug('The buffer             : %s'%buffer)
        self.logger.debug('The exit               : %s'%exit)
        if not os.path.exists(outputDir):
            self.logger.debug("The direcotry [%s] does not exist! Creating it..."%outputDir)
            os.makedirs(outputDir)
        self.tableFile = os.path.join(outputDir,strftime('%b%Y.html'))
        if not os.path.exists(self.tableFile):
            shutil.copytree("csss",os.path.join(outputDir,"csss"))
            f = open(self.tableFile, 'a')
            f.write("""<html><head>
                    <meta http-equiv="Content-Type" content="text/html; charset=utf-8">
                    <link rel="stylesheet" type="text/css" href="csss/framework.css" />
                    </head>
                    <div><a target="_blank" href="../logs">Logs Repository</a></div>
                    <body>
                    <table>
                    <caption>Ion Unit Tests Run During the Month of <b>%s</b></caption>
                    <tr><th>Test</th><th>Test Run Date</th><th>Success</th><th>Failures</th><th>Errors</th><th>Skips</th><th id="topright">Total</th></tr>""" % strftime('%B')) 
            f.close()
        self.testRoot = os.path.abspath(testRoot)
        self.logger.debug("The absolute path for test root is %s"%self.testRoot)
        testRoot = os.getcwd()
        self.logger.debug('The test root          : %s'%testRoot)
        sys.path.insert(0, testRoot)
        utilsDir = os.path.join(testRoot, 'src', 'utils')
        if os.path.exists(utilsDir):
            self.logger.debug('Adding [%s] to path'%utilsDir)
            sys.path.insert(0, utilsDir)
        else:
            self.logger.critical('The utils directory under [%s] is not available!'%testRoot)
        self.catchBreak = catchBreak
        self.verbosity  = 2
        self.failfast   = failfast
        self.buffer     = buffer
        self.exit = exit
        self.timeStamp = strftime('%Y/%m/%d %H:%M:%S')
        self.resultDirName = os.path.join(outputDir,strftime('%B%Y'))
        self.testSuite = {} #unittest.TestSuite()
        self.parallelSuiteList = {}
        if(not os.path.exists(self.resultDirName)):
            self.logger.debug('Directory [%s] to save the test report does not exist. Creating now...'%self.resultDirName)
            os.makedirs(self.resultDirName)
        else:
            self.logger.debug('Directory [%s] to save the test report already exists'%self.resultDirName)
        self.reportName = reportName

        if(not os.path.exists(self.testRoot)):
            self.logger.critical("The test root [%s] does not exist. Nothing to test abort!"%self.testRoot)
            sys.exit(1)

        if(testListFile is not None and os.path.exists(testListFile)):
            self._getAllListTestCases(testListFile)
        else:
            self.logger.debug('The test list file is not available')
            self.__getAllDirectoryTestCases()
        self.logger.debug('Parallel Suite: %s'%self.parallelSuiteList)
        self.logger.debug('Default  Suite: %s'%self.testSuite)

    def __mkTestSuite(self, suite, tList, className, iModule, tName):
        self.logger.debug('Adding Class [%s] to thread [%s]'%(className, tName))
        for test in tList:
            loadName = '%s.%s'%(className, test)
            if not suite.has_key(tName):
                suite[tName] = self.testLoader.loadTestsFromName(loadName, iModule)
                self.logger.debug('Loaded successfully [%s]'%loadName)
            else:
                suite[tName].addTest(self.testLoader.loadTestsFromName(loadName, iModule))
                self.logger.debug('Added successfully [%s]'%loadName)
        self.logger.debug(suite[tName]._tests)      

    def __importModule(self, dName, pName):
        self.logger.debug('Dir Name: [%s] Py File Name: [%s]'%(dName, pName))
        pyNameList = pName.split('.')
        pyName = pyNameList[0]
        if (dName not in sys.path):
            sys.path.insert(0, dName)
        if(pyName == '__init__'):
            moduleName = os.path.dirname(dName)
            sys.path.insert(0, moduleName)
        else:
            moduleName = pyName

        iModule = __import__(moduleName)
        self.logger.debug('Imported [%s] successfully'%moduleName)
        return iModule

    def __loadConfigModule(self, config, moduleName):
        try:
            if config.has_section(moduleName):
                for k,v in config.items(moduleName):
                    self.logger.debug('Adding variable [%s] with value [%s]'%(k, v))
                    self.__setattr__(k, self.__value(v))
        except:
            self.logger.exception(sys.exc_info)

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
                    tmpStr = str.strip(valueStr[1:-1])
                    #self.logger.debug('tmpStr: %s'%tmpStr)
                    tmpList = tmpStr.split(',')
                    return [str.strip(i) for i in tmpList]
                return valueStr

    def __getClass(self, moduleName):
        for name, obj in inspect.getmembers(sys.modules[moduleName]):
            if inspect.isclass(obj):
                return name, obj

    def __getPyList(self, rDir):
        retList = []
        for root, dirs, files in os.walk(rDir):
            for f in files:
                fullpath = os.path.join(root, f)
                if os.path.splitext(fullpath)[1] == '.py':
                    retList.append(fullpath)
        return retList

    def __getAllDirectoryTestCases(self):
        pyList = self.__getPyList(self.testRoot)
        self.logger.debug(pyList)

        for py in pyList:
            dirName = os.path.dirname(py)
            baseName = os.path.basename(py)
            iModule = self.__importModule(dirName, baseName)

            if not self.testSuite.has_key('default'):
                self.testSuite['default'] = self.testLoader.loadTestsFromModule(iModule)
                self.logger.debug('Loaded successfully TestSuite')
            else:
                self.testSuite['default'].addTest(self.testLoader.loadTestsFromModule(iModule))
                self.logger.debug('Added successfully TestSuite')

    def _getAllListTestCases(self, testListFile):
        config = ConfigParser.ConfigParser()
        config.read(testListFile)
        sectionList = config.sections()
        if(len(sectionList) < 1):
            self.logger.error('There were no sections in test list file [%s]'%testListFile)
            raise Exception('There were no sections in test list file [%s]'%testListFile)
        sectionList.sort()
        for module in sectionList:
            self.__loadConfigModule(config, module)
            pyName = self._pyname
            dirName = os.path.join(self.testRoot, module)
            iModule = self.__importModule(dirName, pyName)
            className = self._classname
            
            if(hasattr(self, '_threadname')):
                self.__mkTestSuite(self.parallelSuiteList, self._testlist, className, iModule, self._threadname)
                del(self._threadname)
            else:
                self.__mkTestSuite(self.testSuite, self._testlist, className, iModule, 'default')

    def __insertCurrentReport(self, cReport):
        self.logger.debug('Acquiring lock for file [%s]'%self.tableFile)
        with FileLock(self.tableFile, timeout=3) as lock:
            self.logger.debug('Got lock!')
            with open(self.tableFile, 'a') as tableFile:
                tableFile.write('%s\n'%cReport)
            self.logger.debug('Done updating [%s]'%self.tableFile)

    def runParallelTests(self):
        tList = []
        for key in self.parallelSuiteList.keys():
            t = Thread(group=None, target=self.runTests, name=key, args=(self.parallelSuiteList[key], '[%s]'%key))
            sleep(2)
            self.logger.debug(('Starting Thread [%s]'%key).center(80,'='))
            self.logger.debug('Test Suite: %s'%self.parallelSuiteList[key])
            t.start()
            self.logger.debug('Done'.center(80,'-'))
            tList.append(t)
        for th in tList:
            th.join()

    def runTests(self, testSuite, captionStr):
        self.logger.debug('Starting runTests')
        self.logger.debug('testSuite: %s'%testSuite)
        self.logger.debug('captionStr: %s'%captionStr)
        if self.catchBreak:
            installHandler()
        
        if isinstance(self.testRunner, (type, types.ClassType)):
            try:
                testReportFileName = strftime('iontest_%y%b%d_%H%M%S.html')
                fullTestReportName = os.path.join(self.resultDirName, testReportFileName)
                htmlStream = open(fullTestReportName, 'w')
                htmlStream.write('<html>\n<head>\n<meta http-equiv=\"Content-Type\" content=\"text/html; charset=utf-8\">\n<link rel=\"stylesheet\" type=\"text/css\" href=\"../../framework/csss/framework.css\" />\n</head>\n<body>\n<table border=1>\n')
                htmlStream.write('<div id="infol"><b>Test Run on:</b>%s</div>'%strftime('%d%b,%Y %H:%M:%S'))
                htmlStream.write('<caption>Ion Test Results %s</caption>\n'%captionStr)
                htmlStream.write('<tr><th>Module</th><th>Test Case</th><th>Description</th><th>Result</th><th>Remark</th></tr>')

                testRunner = self.testRunner(stream=htmlStream, verbosity=self.verbosity,
                                             failfast=self.failfast,
                                             buffer=self.buffer)
            except TypeError:
                # didn't accept the verbosity, buffer or failfast arguments
                testRunner = self.testRunner()
        else:
            # it is assumed to be a TestRunner instance
            testRunner = self.testRunner
        self.result = testRunner.run(testSuite)
        success = self.result.testsRun - len(self.result.failures) - len(self.result.errors) - len(self.result.skipped)
        newLine = '<tr><td><a target="_blank" href="%s">%s</a></td><td>%s</td><td><font color="#009966">%s</font></td><td><font color="#FF0000">%s</font></td><td>%s</td><td>%s</td><td><b>%s</b></td></tr>'%(fullTestReportName,
                                                                                                                    '%s [%s]'%(self.reportName, captionStr),
                                                                                                                    self.timeStamp,
                                                                                                                    success,
                                                                                                                    len(self.result.failures),
                                                                                                                    len(self.result.errors),
                                                                                                                    len(self.result.skipped),
                                                                                                                    self.result.testsRun)
        self.__insertCurrentReport(newLine)
        if self.exit:
            sys.exit(not self.result.wasSuccessful())
    
def main():
    parser = argparse.ArgumentParser(description='This script starts a series of tests.')
    parser.add_argument('-r', '--rootDir', help='Mandatory. The location where all of the tests are organized. This is the root directory')
    parser.add_argument('-t', '--testList', help='Optional. This contains the list of the tests to run.')
    parser.add_argument('-o', '--output', help='Optional. This is the output directory.')
    parser.add_argument('-l', '--consoleloglevel', help='Optional. This sets the console log level of the tests to run. Available options are debug, info, warn. Default info')
    parser.add_argument('-n', '--name', help='Optional. This is the name of the report. Default is IonTestReport.')
    parser.add_argument('-c', '--catch', default=False, help='Catch ctrl-C and display results so far', action='store_true')
    parser.add_argument('-f', '--failfast', default=False, help='Stop on first fail or error', action='store_true')
    parser.add_argument('-b', '--buffer', default=False, help='Buffer stdout and stderr during tests', action='store_true')
    parser.add_argument('-d', '--debug', help='Optional. Debug flag.True or False. Default: False', action='store_true', default=False)
    args = parser.parse_args()

    if args.rootDir == None:
        print 'Please specify the directory where the tests are located'
        parser.print_usage()
        sys.exit(1)

    if args.consoleloglevel == None:
        args.consoleloglevel = 'info'

    if args.output == None:
        args.output = '../results'

    if args.debug:
        print 'The option   [-r, --rootDir]         is: %s'%args.rootDir
        print 'The option   [-t, --testList]        is: %s'%args.testList
        print 'The option   [-l, --consoleloglevel] is: %s'%args.consoleloglevel
        print 'The option   [-n, --name]            is: %s'%args.name
        print 'The option   [-o, --output]          is: %s'%args.output
        print 'The option   [-c, --catch]           is: %s'%args.catch
        print 'The option   [-f, --failfast]        is: %s'%args.failfast
        print 'The option   [-b, --buffer]          is: %s'%args.buffer

    it = IonTester(args.rootDir, args.testList, args.consoleloglevel, args.name, args.output, args.catch, args.failfast, args.buffer)

    if (len(it.parallelSuiteList)):
        it.runParallelTests()
    if (len(it.testSuite)):
        it.runTests(it.testSuite['default'], 'From Root Dir [%s]'%it.testRoot)
        
if __name__ == '__main__':
    main()