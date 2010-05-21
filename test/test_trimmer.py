from __future__ import with_statement
import unittest
from util import (output_to_string, input_from_string, args, Test, 
                  mutates_oplog)
import settings
from oplogutils import Trimmer
import re
from pymongo.timestamp import Timestamp


missing = object()


class TrimmerTests(Test):

    def trim(self, answers=None, after='2010-05-10 03:14:29', dry_run=False, 
             expect_code=0, always_yes=False, port=None):
        arglist = ['--host=localhost', '--port=%s' % (port or self.mongo_port)]
        if not answers and answers is not missing:
            answers = ['y']
        if after is not missing:
            if isinstance(after, Timestamp):
                after = self.timestamp_to_arg(after)
            arglist.append('--remove-after='+after)
        if dry_run:
            arglist.append('--dry-run')
        if always_yes:
            arglist.append('-y')
        with input_from_string(''.join(answers or [])):
            return self.run_command(Trimmer, arglist, expect_code)


    def timestamp_to_arg(self, ts):
        return ts.as_datetime().strftime('%Y-%m-%d %H:%M:%S')


    def test_remove_after_required(self):
        s = self.trim(after=missing, expect_code=-1)
        self.assertTrue('Usage:' in s)


    def assertion_error(self, **kwargs):
        try:
            s = self.trim(**kwargs)
        except AssertionError, e:
            return e
        else:
            self.fail('Expected an assertion error.')


    def test_remove_after_is_date(self):
        e = self.assertion_error(after='foo')
        self.assertTrue('Invalid date' in str(e))


    def test_remove_after_must_be_in_the_past(self):
        e = self.assertion_error(after='2037-01-01 13:24:55')
        self.assertTrue('must be in the past' in str(e))


    def assert_does_nothing(self, **kwargs):
        kwargs.setdefault('expect_code', 1)
        s = self.trim(**kwargs)
        self.assertTrue('Doing nothing' in s)


    def test_confirm_answering_no(self):
        self.assert_does_nothing(answers=['n'])


    def count_prompts(self):
        return len(re.findall('Do you want to continue', self.last_output))


    @mutates_oplog
    def test_nonsensical_answer_prompts_again(self):
        self.trim(answers=['x', 'y'])
        self.assertEqual(self.count_prompts(), 2)


    def test_no_is_default(self):
        s = self.trim(answers=['\r'], expect_code=1)
        self.assertTrue('Doing nothing' in s)


    @mutates_oplog
    def test_displays_warning(self):
        self.assertTrue('WARNING' in self.trim())


    @mutates_oplog
    def test_displays_affected_rows(self):
        ms = re.findall('will remove ([0-9]*) events', self.trim())
        self.assertTrue(ms)
        self.assertTrue(int(ms[0]))


    def test_confirm_case_insensitive(self):
        self.assert_does_nothing(answers=['N'])


    @mutates_oplog
    def test_always_yes_skips_confirm(self):
        s = self.trim(always_yes=True)
        self.assertFalse('continue?' in s)


    def test_aborts_if_mongo_running_with_replication_options(self):
        s = self.trim(port=settings.MONGOD_REPLICATION_PORT, expect_code=-1)
        self.assertTrue('without replication options' in s.replace('\n', ' '))


    def trimmed_count(self):
        return self.oplog().find({ 'op': 'n', 'ns': '' }).count()


    def active_count(self):
        return self.oplog().find({ 'ns': { '$ne': '' }, 
                                   'op': { '$ne': 'n' } }).count()


    @mutates_oplog
    def test_removing_all_events(self):
        self.assertTrue(self.active_count())
        self.trim()
        self.assertEqual(self.active_count(), 0)


    @mutates_oplog
    def test_creates_ts_index(self):
        indexes = self.local().system.indexes
        def haveindex():
            return indexes.find({ 'key': { 'ts': 1 } }).count()

        self.assertFalse(haveindex())
        self.trim()
        self.assertTrue(haveindex())


    @mutates_oplog
    def test_remove_some_events(self):
        ts = self.oplog().find().skip(20).limit(1)[0]['ts']
        self.trim(after=ts)
        self.assertTrue(self.active_count())
        self.assertTrue(self.trimmed_count())


    @mutates_oplog
    def test_shows_progress(self):
        s = self.trim()
        self.assertTrue(re.findall('Trimmed [0-9]* events', s, re.M))
