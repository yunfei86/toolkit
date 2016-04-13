# -*- coding: utf-8 -*-

import sys

import time

from dxHTMLTestRunner import ParametrizedTestCase


class OCP50_1(ParametrizedTestCase):
    """ Assay:ocp50 Data:ocp50_1 Mode:AssayDev  """

    MESSAGE = 'test ocp50 assay using data1'

    def test1_vcfComp(self):
        print "======> %s" % (', '.join(map(str, self.param)))
        time.sleep(10)
    def test2_BamComp(self):
        print >>sys.stderr, self.MESSAGE
    def test3_SignalWellComp(self):
        self.fail(self.MESSAGE)
    def test4_BaselineMetricComp(self):
        raise RuntimeError(self.MESSAGE)


