import sys
from StringIO import StringIO


class output_to_string(object):
    debug_output = False 

    def __init__(self):
        self.old = sys.stdout

    def getvalue(self):
        return sys.stdout.getvalue()

    def __enter__(self):
        self.old = sys.stdout
        buf = StringIO()
        if self.debug_output:
            _write = buf.write
            _flush = buf.flush
            def writeboth(*args):
                _write(*args)
                self.old.write(*args)
            def flushboth(*args):
                _flush(*args)
                self.old.flush(*args)
            buf.write = writeboth
            buf.flush = flushboth
        sys.stdout = buf
        return self
        
    def __exit__(self, *args):
        sys.stdout = self.old

    def __str__(self):
        return self.getvalue()
