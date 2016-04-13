# -*- coding: utf-8 -*-

import os

from datetime import datetime

import ionHTMLTestRunner
from  DemoTests.testcase1 import *
from  DemoTests.testcase2 import *
from  DemoTests.testcase3 import *
from  DemoTests.testcase4 import *
import unittest


def touch(fname):
    if os.path.exists(fname):
        os.utime(fname, None)
    else:
        open(fname, 'a').close()

def runTest(suite, directory, title, description):
    if not os.path.exists(directory):
        os.makedirs(directory)

    unittest.TextTestRunner(verbosity=2).run(suite)

    report_file=os.path.join(directory, "TestReport.html")
    touch(report_file)
    outfile = open(report_file,"r+")
    runner = ionHTMLTestRunner.HTMLTestRunner(stream=outfile,title=title,description=description, appendMode=True)
    runner.run(suite)

if __name__ == "__main__":
    DATE = datetime.now().strftime("%Y%m%d%H%M%S") #"201604122314" #sys.argv[1]
    report_directory=os.path.join("./reports", DATE)
    title="Automation Test"
    description="Version: 5.4, Build: Release Candidate 2 (RC2), Server: bleedblue.itw "

    print "1st test running" .center(90,"*")
    suite = unittest.TestSuite()
    suite.addTest(ParametrizedTestCase.parametrize(OCP50_1, param=["passed parameters","mode","/var/www/a","dx"]))
    runTest(suite, report_directory, title, description)

    print "2nd test running" .center(90,"*")
    suite = unittest.TestSuite()
    suite.addTest(ParametrizedTestCase.parametrize(BRCA_1, param=["passed parameters","mode","/var/www/b","dx"]))
    runTest(suite, report_directory, title, description)

    print "3rd test running" .center(90,"*")
    suite = unittest.TestSuite()
    suite.addTest(ParametrizedTestCase.parametrize(DNARNA_1, param=["passed parameters","mode","/var/www/c","dx"]))
    runTest(suite, report_directory, title, description)

    print "4th test running" .center(90,"*")
    suite = unittest.TestSuite()
    suite.addTest(ParametrizedTestCase.parametrize(Lung_1, param=["passed parameters","mode","/var/www/d","dx"]))
    runTest(suite, report_directory, title, description)