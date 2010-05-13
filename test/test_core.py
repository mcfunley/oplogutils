from __future__ import with_statement
import unittest
from oplogutils import _core
from optparse import OptionParser
from util import output_to_string


class CoreTests(unittest.TestCase):
    
    def test_timestamp(self):
        self.assertEqual(_core.timestamp('2010-05-13 00:04:00').time, 
                         1273709040)

    def test_timestamp_fails_invalid(self):
        self.assertRaises(AssertionError, _core.timestamp, 'foo')


    def test_common_options_requires_host(self):
        with output_to_string():
            op = _core.common_options(OptionParser())
            self.assertRaises(SystemExit, op.parse_args, args=[])


    def test_common_options_works_with_all_required_args(self):
        op = _core.common_options(OptionParser())
        try:
            with output_to_string():
                op.parse_args(args=['--host=foo'])
        except SystemExit:
            self.fail('Should not have exited with all required args')

