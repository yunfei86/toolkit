# -*- coding: utf-8 -*-

import unittest

class SampleOutputTestBase(unittest.TestCase):
    """ Base TestCase. Generates 4 test cases x different content type. """
    def test_1(self):
        print self.MESSAGE
    def test_2(self):
        print >>sys.stderr, self.MESSAGE
    def test_3(self):
        self.fail(self.MESSAGE)
    def test_4(self):
        raise RuntimeError(self.MESSAGE)

class SampleTestBasic(SampleOutputTestBase):
    MESSAGE = 'basic test'