import unittest
import axelrod as axl

class TestCyclerParams(unittest.TestCase):
    def setUp(self):
        pass

    def test_default_single_opponent_e2e(self):
        # we know the best stratergy of TitForTat is CCCCCCC...
        opponets = axl.TitForTat()

        #we will set the objewctive to be





