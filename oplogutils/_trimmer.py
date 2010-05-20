import calendar
from datetime import datetime
from pymongo import Connection
from pymongo.timestamp import Timestamp
from optparse import OptionParser, IndentedHelpFormatter
import _core
from _counter import CountQuery
import sys
import tty



class HelpFormatter(IndentedHelpFormatter):
    def format_epilog(self, epilog):
        # don't strip newlines out, etc. 
        return epilog



warning = """
WARNING: Trimming the oplog is destructive. Before performing this procedure, 
you should back up the master database files. 
"""



class Trimmer(_core.Command):
    def get_options(self):
        opts = OptionParser()
        opts.add_option('', '--remove-after', action='store', default=None, 
                        dest='remove_after',
                        help=('The time after which to delete oplog entries. '
                              '(YYYY-MM-DD HH:MM:SS, in UTC).'))
        opts.add_option('-y', '', action='store_true', dest='always_yes', 
                        default=None,
                        help='Answer yes for all prompts.')
        opts.usage = '%prog --host=<host> --remove-after=<date> [options]'
        opts.epilog = """
%s

Examples:

""" % warning

        opts.formatter = HelpFormatter()
        return opts
        

    def validate_options(self):
        if not self.opts.remove_after:
            self.usage_error()

        self.opts.remove_after = _core.timestamp(self.opts.remove_after)

        if self.opts.remove_after.as_datetime() > datetime.now():
            raise AssertionError('--remove-after must be in the past.')


    def should_continue(self):
        if self.opts.always_yes:
            return True

        answer = ''
        while answer not in ['y', 'n']:
            print '\nDo you want to continue? [y/N] ',
            answer = self.getch().lower()
            if answer in ['\r', '\n']:
                return False
            print
        return answer == 'y'


    def run(self):
        self.assert_replication_off()

        q = CountQuery(start=self.opts.remove_after)
        self.affected_events = q.run(self.oplog())

        print warning
        print ('This will remove %d events from the end of the oplog after '
               '%s (UTC).' % (self.affected_events, 
                              self.opts.remove_after.as_datetime()))

        if self.should_continue():
            self.trim()
        else:
            print '\nDoing nothing.'
            sys.exit(1)


    def assert_replication_off(self):
        if self.replication_enabled():
            print """
In order to use this command, the master database must be restarted without
replication options. Back it up and restart it without the --master switch.
"""
            sys.exit(-1)


    def trim(self):
        pass
