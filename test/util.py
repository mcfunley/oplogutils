from __future__ import with_statement
import os
import commands
import subprocess
import time
import socket 
from contextlib import closing
import signal
import sys
from StringIO import StringIO
import unittest
from contextlib import contextmanager


this_dir = os.path.realpath(os.path.dirname(__file__))


class Test(unittest.TestCase):

    def run_command(self, cls, _args, expect_code):
        with args(*_args):
            with output_to_string() as s:
                try:
                    cls().run()
                except SystemExit, e:
                    self.assertEqual(e.code, expect_code)
                else:
                    if expect_code != 0:
                        self.fail('Expected an exit code of %s, but it was 0.' %
                                  expect_code)
                return str(s).strip()


@contextmanager
def dummy():
    yield


class input_from_string(object):
    num = 0

    def __init__(self, string):
        self.string = string
        input_from_string.num += 1
        self.filename = '%s.%s' % (os.path.join(this_dir, 'test.stdin.'), 
                                   input_from_string.num)

    def __enter__(self):
        self.old = sys.stdin
        with open(self.filename, 'w') as f:
            f.write(self.string)

        sys.stdin = open(self.filename, 'r')

    def __exit__(self, *args, **kwargs):
        try:
            os.unlink(self.filename)
        finally:
            sys.stdin = self.old



class output_to_string(object):
    debug_output = False 

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



class args(object):
    def __init__(self, *args):
        self.args = args

    def __enter__(self):
        self.old = sys.argv[:]
        sys.argv = sys.argv[:1]
        sys.argv.extend(self.args)
        
    def __exit__(self, *args):
        sys.argv = self.old


        
class ProcessController(object):
    delay_interval = 0.1
    max_delays = 3000

    def __init__(self, port, name):
        self.port = port
        self.name = name
        name = name.lower()
        self.pidfile = self.logpath('%s.pid' % name)
        self.stderr_file = self.logpath('%s.err' % name)
        self.stdout_file = self.logpath('%s.out' % name)
        self.cwd = os.getcwd()
        self.log = sys.stdout


    def logpath(self, name):
        return os.path.join(this_dir, name)


    def find_executable(self, name):
        return find_executable_in_unix_path(name)


    def __enter__(self):
        self.start()
        return self


    def __exit__(self, *args):
        self.stop()


    def handle_zombie(self):
        raise AssertionError(
            'Port %d is in use, this could be a %s zombie.' % 
            (self.port, self.name))


    def get_command(self):
        raise NotImplemented()

        
    def start(self):
        self.log.write('Starting %s... ' % self.name)
        self.log.flush()

        if self.port_responding():
            self.handle_zombie()

        self.stderr = open(self.stderr_file, 'wb')
        self.stdout = open(self.stdout_file, 'wb')

        self.proc = subprocess.Popen(
            self.get_command(), stdin=None, stderr=self.stderr, 
            stdout=self.stdout, cwd=self.cwd)
        for i in range(self.max_delays):
            time.sleep(self.delay_interval)
            if self.server_up():
                break

        if not self.server_up():
            raise AssertionError('%s failed to start. Error: \n\n%s' %
                                 (self.name, self.read_stderr()))

        with open(self.pidfile, 'wb') as f:
            f.write(str(self.proc.pid))
        
        self.log.write('done.\n')
        self.log.flush()


    def server_up(self):
        p = self.proc.poll()
        if p != None:
            if p < 0:
                msg = '%s was terminated by a signal (%d).' % (self.name, p)
            else:
                msg = '%sn terminated unexpectedly (return code %d).' % (
                    self.name, p)
            raise AssertionError('%s\%s stderr output:\n%s' % (
                    self.name, msg, self.read_stderr()))
            return False
        return self.port_responding()


    def port_responding(self):
        try:
            with closing(socket.socket(socket.AF_INET, socket.SOCK_STREAM)) as s:
                s.connect(('localhost', self.port))
        except socket.error, e:
            return False
        return True

    
    def read_stdout(self):
        with open(self.stdout_file, 'rb') as f:
            return f.read()
    

    def read_stderr(self):
        with open(self.stderr_file, 'rb') as f:
            return f.read()


    def stop(self):
        pid = self.pid()
        try:
            os.kill(pid, signal.SIGTERM)
            waitpid_guard_eintr(pid)
            os.remove(self.pidfile)
        finally:
            try:
                self.stderr.close()
            finally:
                self.stdout.close()


    def pid(self):
        with open(self.pidfile) as f:
            return int(f.read())


def waitpid_guard_eintr(pid):
    """
    Waits for pid to exit, and retries on EINTR. See:
    http://mail.python.org/pipermail/python-dev/2004-November/049983.html
    """
    while True:
        try:
            return os.waitpid(pid, 0)
        except OSError, e:
            if e.errno == errno.EINTR:
                continue
            raise


def find_executable_in_unix_path(name): 
    """
    Returns the full path to an executable given just its name. 
    """
    # Fails on darwin for the same reasons as waitpid.  
    while True: 
        try: 
            return commands.getoutput('which %s' % name).strip() 
        except IOError, e: 
            if e.errno == errno.EINTR: 
                continue 
            raise 
