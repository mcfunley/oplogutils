import _core
from optparse import OptionParser
import sys


def Options(*args):
    opts = OptionParser()
    _core.common_options(opts)
    opts.add_option('', '--start', action='store', default=None,
                    help=('The starting time (YYYY-MM-DD HH:MM:SS, UTC time).'))
    opts.add_option('', '--end', action='store', default=None, 
                    help=('The ending time.'))
    opts.usage = '%prog --host=<host> [options]'
    opts.epilog = """Counts the number of oplog events between <start> and <end>, if provided. 
The range is open-ended if only one or zero of the <start> and <end> parameters
are provided. 
"""
    return opts



class Counter(_core.Command):
    options_cls = Options

    def run(self):
        oplog = self.oplog()
        start, end = self.opts.start, self.opts.end
        if not (start or end):
            print oplog['$main'].count(), 'events in the oplog.'
        else:
            q = self.get_query(start, end)
            events = oplog['$main'].find({ 'ts': q }).count()
            print events, 'events in the oplog',
            if start and end:
                print 'between', start, 'and', end,
            elif start:
                print 'after', start, 
            else:
                print 'before', end, 
            print '(UTC).'


    def get_query(self, start, end):
        q = {}
        if start:
            start = _core.timestamp(start)
            q.update({ '$gte':  start })
        if end:
            end = _core.timestamp(end)
            if start and end.as_datetime() < start.as_datetime():
                print 'The start date must be before the end date.'
                sys.exit(-1)
            q.update({ '$lte':  end })
        return q
