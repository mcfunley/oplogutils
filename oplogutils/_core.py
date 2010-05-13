import calendar 
from datetime import datetime
from pymongo.timestamp import Timestamp
import re
import sys

def _num(n):
    return '([0-9]{%d,})' % n

_date_re = '%s-%s-%s %s:%s:%s' % tuple(map(_num, [4, 2, 2, 2, 2, 2]))


def timestamp(string_date):
    m = re.match(_date_re, string_date)
    if not m:
        msg = 'Invalid date: %s (use format: YYYY-MM-DD HH:MM:SS)' % string_date
        raise AssertionError(msg)
    d = datetime(*map(int, m.groups()))
    return Timestamp(calendar.timegm(d.timetuple()), 0)



def common_options(op):
    op.add_option('', '--host', action='store', dest='host', default=None, 
                  help='The hostname of the mongodb master instance.')
    op.add_option('', '--port', action='store', dest='port', type='int', 
                  default=27017, 
                  help=('The port of the mongodb master instance. (Defaults '
                        'to 27017.)'))

    original_parse = op.parse_args

    def check_required(*args, **kwargs):
        opts, args = original_parse(*args, **kwargs)
        if not opts.host:
            op.print_help()
            sys.exit(-1)
        return opts, args
    
    op.parse_args = check_required
    return op
