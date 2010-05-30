from __future__ import with_statement
import unittest
from util import output_to_string, args, Test, mutates_oplog
import settings
from oplogutils import Counter
import re
from datetime import datetime, timedelta

re_start = '([0-9]*) events in the oplog'


class CounterTests(Test):

    def count(self, *args, **kwargs):
        expect_code = kwargs.get('expect_code', 0)
        args = list(args)
        args.extend(['--port=%s' % self.mongo_port,
                     '--host=localhost',])
        return self.run_command(Counter, args, expect_code)


    def assertPos(self, match):
        self.assertTrue(int(match.groups()[0]))


    def assertZero(self, match):
        self.assertFalse(int(match.groups()[0]))


    def test_no_args(self):
        m = re.match(re_start+'.', self.count())
        self.assertTrue(m)
        self.assertPos(m)


    def matchAfter(self, start):
        return re.match(re_start + ' after (.*) \(UTC\)\.', 
                        self.count('--start=%s' % start))


    def afterTest(self, start, expectNum):
        m = self.matchAfter(start)
        self.assertTrue(m)
        expectNum(m)
        self.assertEqual(m.groups()[1], start)


    def test_start_only(self):
        self.afterTest('2010-05-13 00:00:01', self.assertPos) 

    
    def test_start_future(self):
        # Would make this ludicrously more distant but pymongo.timestamp
        # requires an int time (not a long). 
        self.afterTest('2035-05-13 00:00:01', self.assertZero)

    
    def beforeTest(self, end, expectNum):
        m = re.match(re_start + ' before (.*) \(UTC\)\.', 
                     self.count('--end=%s' % end))
        self.assertTrue(m)
        expectNum(m)
        self.assertEqual(m.groups()[1], end)


    def test_end_only(self):
        self.beforeTest('2035-05-13 00:00:01', self.assertPos)

    
    def test_end_remote_past(self):
        self.beforeTest('1979-06-29 04:37:42', self.assertZero)


    def test_end_before_start(self):
        self.assertEqual(
            self.count('--start=2010-05-10 00:00:01', 
                       '--end=2010-05-03 00:00:01', 
                       expect_code=-1),
            'The start date must be before the end date.') 


    def test_start_and_end(self):
        d = self.oplog().find_one()['ts'].as_datetime()
        day = timedelta(1)
        start = str(d - day)[:19]
        end = str(d + day)[:19]
        m = re.match(re_start + ' between (.*) and (.*) \(UTC\)\.', 
                     self.count('--start=%s' % start, '--end=%s' % end))
        self.assertTrue(m)
        self.assertPos(m)
        gs = m.groups()
        self.assertEqual(gs[1], start)
        self.assertEqual(gs[2], end)

