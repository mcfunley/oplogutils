import _core
from optparse import OptionParser
import sys



class CountQuery(dict):
    def __init__(self, start=None, end=None):
        if start:
            start = self.as_timestamp(start)
            self.update({ '$gte':  start })
        if end:
            end = self.as_timestamp(end)
            if start and end.as_datetime() < start.as_datetime():
                print 'The start date must be before the end date.'
                sys.exit(-1)
            self.update({ '$lte':  end })

    def as_timestamp(self, x):
        if isinstance(x, basestring):
            return _core.timestamp(x)
        return x

    def run(self, oplog):
        return oplog['$main'].find({ 'ts': self }).count()



class Counter(_core.Command):

    def get_options(self):
        opts = OptionParser()
        opts.add_option('', '--start', action='store', default=None,
                         help=('The starting time (YYYY-MM-DD HH:MM:SS, '
                               'UTC time).'))
        opts.add_option('', '--end', action='store', default=None, 
                        help=('The ending time.'))
        opts.usage = '%prog --host=<host> [options]'
        opts.epilog = """Counts the number of oplog events between <start> and <end>, if provided. 
The range is open-ended if only one or zero of the <start> and <end> parameters
are provided. 
"""
        return opts


    def run(self):
        oplog = self.oplog()
        start, end = self.opts.start, self.opts.end
        if not (start or end):
            print oplog['$main'].count(), 'events in the oplog.'
        else:
            q = CountQuery(start, end)
            events = q.run(oplog)
            print events, 'events in the oplog',
            if start and end:
                print 'between', start, 'and', end,
            elif start:
                print 'after', start, 
            else:
                print 'before', end, 
            print '(UTC).'

