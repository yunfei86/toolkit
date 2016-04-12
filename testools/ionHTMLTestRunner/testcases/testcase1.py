# -*- coding: utf-8 -*-

import unittest

class SampleTest1(unittest.TestCase):
    """ A class that fails.

    This simple class has only one test case that fails.
    """
    def test_fail(self):
        """
        test description ("aaaaaaaaa")
        """
        self.fail()
