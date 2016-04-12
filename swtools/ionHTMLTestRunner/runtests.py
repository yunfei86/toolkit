# -*- coding: utf-8 -*-

import StringIO, sys, unittest, os
import ionHTMLTestRunner
from  testcases.testcase1 import SampleTest1
from  testcases.testcase2 import SampleTest2
from  testcases.testcase3 import SampleTestBasic

def touch(fname):
    if os.path.exists(fname):
        os.utime(fname, None)
    else:
        open(fname, 'a').close()


if __name__ == "__main__":
    
    DATE = "20160420" #sys.argv[1]
    
    suite = unittest.TestSuite()
    
    suite.addTests([
            unittest.defaultTestLoader.loadTestsFromTestCase(SampleTest1),
            unittest.defaultTestLoader.loadTestsFromTestCase(SampleTest2),
            unittest.defaultTestLoader.loadTestsFromTestCase(SampleTestBasic)])
    
    directory=os.path.join("./reports", DATE)
    if not os.path.exists(directory):
        os.makedirs(directory)
    
    unittest.TextTestRunner(verbosity=2).run(suite)

    report_file=os.path.join(directory, "TestReport.html")
    touch(report_file)
    outfile = open(report_file,"r+")
    print os.path.join(directory, "TestReport.html")
    runner = ionHTMLTestRunner.HTMLTestRunner(stream=outfile,title='This is A Test Report',description='This is a demonstration', appendMode=True)
    runner.run(suite)