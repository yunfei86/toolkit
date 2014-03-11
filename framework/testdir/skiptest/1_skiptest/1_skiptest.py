"""
This module is part of the example code to demo the conditional skipping. This is
the first module where a test flag file is created for the future check in the
second module 2_skiptest.py in the directory 2_skiptest.
"""
import sys, os, ionunittest

from ionsystem    import IonSystem
from stopwatch    import StopWatch
from re           import search
from time         import sleep

import subprocess


class DeploymentTest(ionunittest.TestCase):

    def localInit(self):
        """
        This method is a local initialization method. The instance variables could be
        initialized. The stopWatch, ionSystem and tsInstaller are initialized in this
        method.
        @rtype: void
        @return: None.
        """
        self.logger.info('Local Init called')
        self.stopWatch = StopWatch()
        self.ionSystem = IonSystem()
        if os.path.exists('/tmp/testflag'):
            self.ionSystem.execute('rm /tmp/testflag')
    
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

    def test1_dummy(self):
        """
        This is a dummy method.
        """
        self.logger.info('test1_dummy')
        
    def test2_genflag(self):
        """
        This method creates the test flag file to be tested in the future. Take precaution
        to check the existance of the test flag.
        """
        self.assertFalse(os.path.exists('/tmp/testflag'), "Oops the file /tmp/testflag Exists!")
        self.ionSystem.execute('touch /tmp/testflag')
        self.logger.info('The file exists: %s'%os.path.exists('/tmp/testflag'))
        