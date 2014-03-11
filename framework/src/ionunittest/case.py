import ConfigParser
import os, sys, inspect

verNum = float(sys.version.split()[0][:-2])

if 2.4 <= verNum <= 2.6:
    import unittest2 as unittest
else:
    import unittest

utilpath = os.path.join('src','utils')
if utilpath not in sys.path:
    sys.path.insert(0, utilpath)

from logbase import LogBase

class TestCase(unittest.TestCase):
    if os.path.exists(os.path.join(os.getcwd(),'debug.txt')):
        f = open(os.path.join(os.getcwd(),'debug.txt'), 'r')
        debugLevelStr = f.readline()
        debugLevel = debugLevelStr.strip()
        logBase = LogBase('IonUnitTest', debugLevel)
    else:
        logBase = LogBase('IonUnitTest')

    logBase.createRotatingFileLogger('log/ionunittest.log')
    logger = logBase.logger
    
    config = ConfigParser.ConfigParser()

    def __init__(self, methodName='runTest'):
        """Create an instance of the class that will use the named test
           method when executed. Raises a ValueError if the instance does
           not have a method with the specified name.
        """
        super(TestCase, self).__init__(methodName)
        self.addRemark = ''
        self.__loadConfigFile()
        self.localInit()

    def __loadConfigFile(self):
        """
        This is a private method which finds a config file with the name of <classfile>.cfg and loads
        the values from it and makes it available to the test case magicaly.
        """
        configFileName =  os.path.splitext(inspect.getfile(self.__class__))[0]
        if configFileName == '' or configFileName == None:
            self.logger.error('Could not find the name of the config file!')
            return
        configFileName += '.cfg'
        if os.path.exists(configFileName):
            try:
                self.logger.debug('Config file [%s] exists'%configFileName)
                self.config.read(configFileName)
                if self.config.has_section('AutoValues'):
                    for k,v in self.config.items('AutoValues'):
                        self.logger.debug('Adding variable [%s] with value [%s]'%(k, v))
                        self.__setattr__(k, self.__value(v))
            except:
                self.logger.exception(sys.exc_info)
        else:
            self.logger.debug('Config file [%s] does not exist'%configFileName)

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
                    self.logger.debug('tmpStr: %s'%tmpStr)
                    tmpList = tmpStr.split(',')
                    return [str.strip(i) for i in tmpList]
                return valueStr

    def localInit(self):
        """
        This is a public method to be over ridden by the testcase to provide a local initialization method.
        User could bring in a whole lot of instance variables through this method.
        """
        pass

#http://eli.thegreenplace.net/2011/08/02/python-unit-testing-parametrized-test-cases/    
#
#import unittest
#
#class ParametrizedTestCase(unittest.TestCase):
#    """ TestCase classes that want to be parametrized should
#        inherit from this class.
#    """
#    def __init__(self, methodName='runTest', param=None):
#        super(ParametrizedTestCase, self).__init__(methodName)
#        self.param = param
#
#    @staticmethod
#    def parametrize(testcase_klass, param=None):
#        """ Create a suite containing all tests taken from the given
#            subclass, passing them the parameter 'param'.
#        """
#        testloader = unittest.TestLoader()
#        testnames = testloader.getTestCaseNames(testcase_klass)
#        suite = unittest.TestSuite()
#        for name in testnames:
#            suite.addTest(testcase_klass(name, param=param))
#        return suite