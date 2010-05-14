from __future__ import with_statement
import unittest
from threading import Thread, Event
from util import output_to_string, input_from_string, args, Test
import settings


class TrimmerTests(Test):

    def default_args(self):
        return ['--remove-after=2010-05-10 03:14:29', '--host=localhost', 
                '--port=%s' % settings.MONGOD_PORT]


    def trim(self, arglist, answers, expect_code=0):
        if arglist is None:
            arglist = self.default_args()
        with input_from_string(''.join(answers)):
            return self.run_command(Trimmer, arglist, expect_code)


    def test_dry_run_does_not_commit_changes(self):
        pass


    def test_remove_after_required(self):
        pass


    def test_remove_after_must_be_past(self):
        pass


    def test_confirm_answering_no(self):
        pass


    def test_confirm_defaults_to_no(self):
        pass


