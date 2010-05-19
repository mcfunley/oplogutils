from __future__ import with_statement
import unittest
from threading import Thread, Event
from util import output_to_string, input_from_string, args, Test
import settings
from oplogutils import Trimmer


missing = object()


class TrimmerTests(Test):

    def trim(self, answers=None, after='2010-05-10 03:14:29', dry_run=False, 
             expect_code=0):
        arglist = ['--host=localhost', '--port=%s' % settings.MONGOD_PORT]
        if not answers and answers is not missing:
            answers = ['y']
        if after is not missing:
            arglist.append('--remove-after='+after)
        if dry_run:
            arglist.append('--dry-run')
        with input_from_string(''.join(answers or [])):
            return self.run_command(Trimmer, arglist, expect_code)


    def test_dry_run_does_not_commit_changes(self):
        pass


    def test_remove_after_required(self):
        s = self.trim(after=missing, expect_code=-1)
        self.assertTrue('Usage:' in s)


    def test_remove_after_is_date(self):
        self.assertRaises(AssertionError, self.trim, after='foo')


    def test_remove_after_must_be_in_the_past(self):
        pass


    def test_confirm_answering_no(self):
        pass


    def test_confirm_defaults_to_no(self):
        pass


    def test_removing_events(self):
        pass

