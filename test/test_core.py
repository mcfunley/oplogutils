import unittest
from oplogutils import _core


class CoreTests(unittest.TestCase):
    
    def test_timestamp(self):
        self.assertEqual(_core.timestamp('2010-05-13 00:04:00').time, 
                         1273709040)




