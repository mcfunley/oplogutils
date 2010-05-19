import calendar 
from datetime import datetime
from pymongo.timestamp import Timestamp
from pymongo import Connection
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



class Command(object):

    def __init__(self):
        self.option_parser = self.get_options()
        self.common_options(self.option_parser)
        self.opts, self.args = self.option_parser.parse_args()

        if not self.opts.host:
            self.usage_error()

        self.validate_options()


    def usage_error(self):
        self.option_parser.print_help()
        sys.exit(-1)


    def common_options(self, op):
        op.add_option('', '--host', action='store', dest='host', default=None, 
                      help='The hostname of the mongodb master instance.')
        op.add_option('', '--port', action='store', dest='port', type='int', 
                      default=27017, 
                      help=('The port of the mongodb master instance. (Defaults '
                            'to 27017.)'))
        return op


    def get_options(self):
        raise NotImplementedError()


    def validate_options(self):
        pass

    
    def oplog(self):
        return Connection(self.opts.host, self.opts.port).local.oplog


    def run(self):
        raise NotImplementedError()
