# -*- coding: utf-8 -*-

import unittest

class SampleTest2(unittest.TestCase):
    """ A class that passes.

    This simple class has only one test case that passes.
    """
    def __init__(self, methodName):
        unittest.TestCase.__init__(self, methodName)

    def test_pass_no_output(self):
        """        test description
        """
        pass