# -*- coding: utf-8 -*-

import sys
import time

from dxHTMLTestRunner import ParametrizedTestCase


class BRCA_1(ParametrizedTestCase):
    """ Assay:BRCA Data:brca_1 Mode:AssayDev  """

    MESSAGE = 'test brca assay using data1'

    def test1_vcfComp(self):
        time.sleep(5)
        print "======> %s" % (', '.join(map(str, self.param)))
    def test2_BamComp(self):
        print >>sys.stderr, self.MESSAGE
    def test3_SignalWellComp(self):
        self.fail(self.MESSAGE)
    def test4_BaselineMetricComp(self):
        raise RuntimeError(self.MESSAGE)

