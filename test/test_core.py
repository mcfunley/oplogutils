from __future__ import with_statement
import unittest
from oplogutils import _core
from optparse import OptionParser
from util import output_to_string, args


class MockCommand(_core.Command):
    def get_options(self):
        return OptionParser()

    def validate_options(self):
        pass

    def run(self):
        pass



class CoreTests(unittest.TestCase):

    def test_timestamp(self):
        self.assertEqual(_core.timestamp('2010-05-13 00:04:00').time, 
                         1273709040)

    def test_timestamp_fails_invalid(self):
        self.assertRaises(AssertionError, _core.timestamp, 'foo')


    def test_host_required(self):
        with output_to_string():
            with args():
                self.assertRaises(SystemExit, MockCommand)


    def test_common_options_works_with_all_required_args(self):
        with output_to_string():
            with args('--host=foo'):
                try:
                    MockCommand().run()
                except SystemExit:
                    self.fail('Should not have exited with all required args')

