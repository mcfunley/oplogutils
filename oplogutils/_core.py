import calendar 
from datetime import datetime
from pymongo.timestamp import Timestamp
import re

def _num(n):
    return '([0-9]{%d,})' % n

date_re = '%s-%s-%s %s:%s:%s' % tuple(map(_num, [4, 2, 2, 2, 2, 2]))


def timestamp(string_date):
    m = re.match(date_re, string_date)
    if not m:
        msg = 'Invalid date: %s (use format: YYYY-MM-DD HH:MM:SS)' % string_date
        raise AssertionError(msg)
    d = datetime(*map(int, m.groups()))
    return Timestamp(calendar.timegm(d.timetuple()), 0)

