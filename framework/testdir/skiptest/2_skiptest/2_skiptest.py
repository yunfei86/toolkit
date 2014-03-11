import sys, os, ionunittest

from ionsystem    import IonSystem
from stopwatch    import StopWatch
from re           import search
from time         import sleep

#def skipCondition():
#    ionSystem = IonSystem()
#    ionSystem.execute('ls /tmp/testflag')
#    print '='*80
#    print 'output is = ',ionSystem.getStdOut()
#    print 'error is  = ',ionSystem.getStdErr()
#    print '-'*80
#    return ionSystem.getStdOut() == '/tmp/testflag'

skipCondition = lambda fName: os.path.exists(fName)
        
class DeploymentTest(ionunittest.TestCase):

    def localInit(self):
        """
        This method is a local initialization method. The instance variables could be
        initialized. The stopWatch, ionSystem and tsInstaller are initialized in this
        method.
        @rtype: void
        @return: None.
        """
        self.logger.debug('Local Init called')
        self.stopWatch = StopWatch()
        self.ionSystem = IonSystem()

    def setUp(self):
        """
        This method is called before each and every test case. This method could
        be used to setup the test fixture. Currently a stop watch is called to
        record the start of the test case.

        @rtype: void
        @return: None.
        """
        self.stopWatch.startTimer()
        self.logger.info('='*80)
        self.logger.info('Setup test fixture for [%s]'%self.id())
        self.logger.info('='*80)

    def tearDown(self):
        """
        This method is called after each and every test case. This method could
        be used to clean-up after the test case. The stop watch is stopped and
        the time delta is used to print out the time consumed by the test case.

        @rtype: void
        @return: None.
        """
        self.stopWatch.stopTimer()
        self.logger.info('Time taken to complete [%s] is [%s]'%(self.id(), self.stopWatch.getTimeDelta()))
        self.logger.debug('Tear down test fixture for [%s]'%self.id())
        self.logger.info('Done'.center(80,'-'))

    def test1_dummy_second(self):
        self.logger.info('test1_dummy_second')
    
    @ionunittest.skipIf(skipCondition('/tmp/testflag'), 'Test skipped!')
    def test2_skiptest(self):
        self.logger.info('This output should not appear!')
        
    def test3_skipinternaltest(self):
        if skipCondition('/tmp/testflag'):
            self.logger.info('test3_skipinternaltest: This is now skipped in test3!')
            return
        
        self.logger.info('This output should not appear too!')
