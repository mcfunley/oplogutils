import calendar
from datetime import datetime
from pymongo import Connection
from pymongo.timestamp import Timestamp
from optparse import OptionParser
import _core


class Trimmer(_core.Command):
    def get_options(self):
        opts = OptionParser()
        opts.add_option('', '--remove-after', action='store', default=None, 
                        dest='remove_after',
                        help=('The time after which to delete oplog entries. '
                              '(YYYY-MM-DD HH:MM:SS, in UTC).'))
        opts.add_option('', '--dry-run', action='store_true', default=False, 
                        dest='dry_run',
                        help=('Emit output explaining changes that would occur, '
                              'but do not delete any oplog entries.'))
        opts.add_option('-y', '', action='store_true', dest='always_yes', 
                        default=None,
                        help='Answer yes for all prompts.')
        opts.usage = '%prog --host=<host> --remove-after=<date> [options]'
        opts.epilog = """
WARNING: Trimming the oplog is destructive. Before performing this
procedure, you should back up the master database files. 

Examples:

"""
        return opts
        

    def validate_options(self):
        if not self.opts.remove_after:
            self.usage_error()

        self.opts.remove_after = _core.timestamp(self.opts.remove_after)

            


