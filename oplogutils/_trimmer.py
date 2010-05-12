import calendar
from datetime import datetime
from pymongo import Connection
from pymongo.timestamp import Timestamp
from optparse import OptionParser


def Options():
    opts = OptionParser()
    opts.add_option('', '--host', action='store', dest='host', default=None, 
                    help='The hostname of the mongodb master instance.')
    opts.add_option('', '--port', action='store', dest='port', type='int', 
                    default=27017, 
                    help=('The port of the mongodb master instance. (Defaults '
                          'to 27017'))
    opts.add_option('', '--remove-after', action='store', default=None, 
                    help=('The time after which to delete oplog entries. '
                          '(YYYY-MM-DD HH:MM:SS, in UTC).'))
    opts.add_option('', '--dry-run', action='store_true', default=False, 
                    help=('Emit output explaining changes that would occur, '
                          'but do not delete any oplog entries.'))
    opts.usage = '%prog --host=<host> --remove-after=<date> [options]'
    opts.epilog = """
Examples:
  trim-oplog 
"""
    opts, args = opts.parse_args()
    return opts, args


class Trimmer(object):
    def __init__(self):
        self.opts, self.args = Options()

    def run(self):
        self.warn_backup()

    def warn_backup(self):
        print '\nWARNING:\n--------\n'
        print """
Trimming the oplogis destructive. Before performing this procedure, you should 
back up 
"""


