# -*- coding: utf-8 -*-

import sys
import time

from ionHTMLTestRunner import ParametrizedTestCase


class Lung_1(ParametrizedTestCase):
    """ Assay:AmplisqSeqLung Data:AmpliSeqLung_4 Mode:AssayDev  """

    MESSAGE = 'test AplisSeq lung assay using data1'

    def test1_vcfComp(self):
        time.sleep(5)
        print "======> %s" % (', '.join(map(str, self.param)))
    def test2_BamComp(self):
        print >>sys.stderr, self.MESSAGE
    def test3_SignalWellComp(self):
        self.fail(self.MESSAGE)
    def test4_BaselineMetricComp(self):
        raise RuntimeError(self.MESSAGE)