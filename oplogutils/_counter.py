import _core
from optparse import OptionParser


def options():
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
    return opts.parse_args()



class Counter(object):
    def __init__(self):
        self.opts, self.args = options()

    def run(self):
        pass
