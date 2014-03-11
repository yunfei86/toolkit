"""Running tests"""

import sys,os
import time

verNum = float(sys.version.split()[0][:-2])

if 2.4 <= verNum <= 2.6:
    from unittest2 import result
else:
    from unittest import result

from .signals import registerResult

__unittest = True

class _WritelnDecorator(object):
    """Used to decorate file-like objects with a handy 'writeln' method"""
    def __init__(self,stream):
        self.stream = stream

    def __getattr__(self, attr):
        if attr in ('stream', '__getstate__'):
            raise AttributeError(attr)
        return getattr(self.stream,attr)

    def writeln(self, arg=None):
        if arg:
            self.write(arg)
        self.write('\n') # text-mode streams translate to \r\n if needed


class HtmlTestResult(result.TestResult):
    """A test result class that can print formatted text results to a stream.

    Used by TextTestRunner.
    """
    separator1 = '=' * 70
    separator2 = '-' * 70

    def __init__(self, stream, descriptions, verbosity):
        super(HtmlTestResult, self).__init__()
        self.stream = stream
        self.showAll = verbosity > 1
        self.dots = verbosity == 1
        self.descriptions = descriptions

    def getDescription(self, test):
        doc_first_line = test.shortDescription()
        if self.descriptions and doc_first_line:
            return '\n'.join((str(test), doc_first_line))
        else:
            return str(test)
        
    def getModuleInfo(self, test):
        infoList = str(test).split()
        if(len(infoList) == 2):
            return infoList[1][1:-1]
        return infoList

    def startTest(self, test):
        super(HtmlTestResult, self).startTest(test)
        #print self.getModuleInfo(test)
        if self.showAll:
            self.stream.write('<tr><td>%s</td><td>%s</td><td>%s</td>'%(self.getModuleInfo(test),test._testMethodName,test._testMethodDoc))
            #self.stream.write(self.getDescription(test))
            #self.stream.write(" ... ")
            self.stream.flush()

    def addSuccess(self, test):
        super(HtmlTestResult, self).addSuccess(test)
        if self.showAll:
            self.stream.writeln("<td>OK</td><td>%s</td></tr>"%test.addRemark)
            test.addRemark = ''
            #self.stream.writeln("ok")
        elif self.dots:
            self.stream.write('.')
            self.stream.flush()

    def addError(self, test, err):
        super(HtmlTestResult, self).addError(test, err)
        if self.showAll:
            print
            print '='*80
            print 'The following error occured:'
            print '_'*80
            print self._exc_info_to_string(err, test)
            print '.'*80
            self.stream.writeln("<td>ERROR</td><td><div class=redText>%s</div></td></tr>"%self._exc_info_to_string(err, test).replace("\n","<br/>"))
        elif self.dots:
            self.stream.write('E')
            self.stream.flush()

    def addFailure(self, test, err):
        super(HtmlTestResult, self).addFailure(test, err)
        if self.showAll:
            if(len(test.addRemark)):
                self.stream.writeln("<td>FAIL</td><td><div class=blueText>%s</div><br/><br/><div class=redText>%s</div></td></tr>"%(test.addRemark, self._exc_info_to_string(err, test).replace("\n","<br/>")))
            else:
                self.stream.writeln("<td>FAIL</td><td><div class=redText>%s</div></td></tr>"%self._exc_info_to_string(err, test).replace("\n","<br/>"))
        elif self.dots:
            self.stream.write('F')
            self.stream.flush()

    def addSkip(self, test, reason):
        super(HtmlTestResult, self).addSkip(test, reason)
        if self.showAll:
            self.stream.writeln("<td>Skipped</td><td>%s</td></tr>"%reason)
        elif self.dots:
            self.stream.write("s")
            self.stream.flush()

    def addExpectedFailure(self, test, err):
        super(HtmlTestResult, self).addExpectedFailure(test, err)
        if self.showAll:
            self.stream.writeln("<td>expected failure</td><td>%s</td></tr>"%err)
        elif self.dots:
            self.stream.write("x")
            self.stream.flush()

    def addUnexpectedSuccess(self, test):
        super(HtmlTestResult, self).addUnexpectedSuccess(test)
        if self.showAll:
            self.stream.writeln("<td>unexpected success</td><td></td></tr>")
        elif self.dots:
            self.stream.write("u")
            self.stream.flush()

    def printErrors(self):
        if self.dots or self.showAll:
            self.stream.writeln()
        #self.printErrorList('ERROR', self.errors)
        #self.printErrorList('FAIL', self.failures)

    def printErrorList(self, flavour, errors):
        for test, err in errors:
            self.stream.writeln(self.separator1)
            self.stream.writeln("%s: %s" % (flavour,self.getDescription(test)))
            self.stream.writeln(self.separator2)
            self.stream.writeln("%s" % err)


class HtmlTestRunner(object):
    """A test runner class that displays results in textual form.

    It prints out the names of tests as they are run, errors as they
    occur, and a summary of the results at the end of the test run.
    """
    resultclass = HtmlTestResult

    def __init__(self, stream=sys.stderr, descriptions=True, verbosity=1,
                 failfast=False, buffer=False, resultclass=None):
        self.stream = _WritelnDecorator(stream)
        self.descriptions = descriptions
        self.verbosity = verbosity
        self.failfast = failfast
        self.buffer = buffer
        if resultclass is not None:
            self.resultclass = resultclass

    def _makeResult(self):
        return self.resultclass(self.stream, self.descriptions, self.verbosity)

    def run(self, test):
        "Run the given test case or test suite."
        result = self._makeResult()
        registerResult(result)
        result.failfast = self.failfast
        result.buffer = self.buffer
        startTime = time.time()
        startTestRun = getattr(result, 'startTestRun', None)
        if startTestRun is not None:
            startTestRun()
        try:
            test(result)
        finally:
            print "All Tests Are Complted".center(80, '=')
            stopTestRun = getattr(result, 'stopTestRun', None)
            if stopTestRun is not None:
                stopTestRun()
        stopTime = time.time()
        timeTaken = stopTime - startTime
        self.stream.writeln('</table>\n')
        #result.printErrors()
        #if hasattr(result, 'separator2'):
        #    self.stream.writeln(result.separator2)
        run = result.testsRun

        self.stream.writeln("<div id=\"info\">Ran %d test%s in %.3fs</div>" %
                            (run, run != 1 and "s" or "", timeTaken))

        expectedFails = unexpectedSuccesses = skipped = 0
        try:
            results = map(len, (result.expectedFailures,
                                result.unexpectedSuccesses,
                                result.skipped))
        except AttributeError:
            pass
        else:
            expectedFails, unexpectedSuccesses, skipped = results

        infos = []
       
        if not result.wasSuccessful():
            self.stream.write("<div id=\"info\">FAILED")
            failed, errored = map(len, (result.failures, result.errors))
            if failed:
                infos.append("failures=%d" % failed)
            if errored:
                infos.append("errors=%d" % errored)
        else:
            self.stream.write("<div id=\"info\">OK</div>")
        if skipped:
            infos.append("skipped=%d" % skipped)
        if expectedFails:
            infos.append("expected failures=%d" % expectedFails)
        if unexpectedSuccesses:
            infos.append("unexpected successes=%d" % unexpectedSuccesses)
        if infos:
            self.stream.writeln(" (%s)" % (", ".join(infos),))
        else:
            self.stream.write("\n")
        self.stream.writeln('</div></body></html>\n')
        return result
