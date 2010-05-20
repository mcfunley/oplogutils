from __future__ import with_statement
from contextlib import contextmanager
import os
from setuptools.command.test import ScanningLoader
import unittest
import commands
from util import ProcessController
import settings
from pymongo import Connection
import shutil
import tarfile



this_dir = os.path.realpath(os.path.dirname(__file__))

def filename(n):
    return os.path.join(this_dir, n)


class FixtureData(object):
    def __init__(self):
        self.fixtures = filename('fixtures')
        self.fixtures_replication = filename('fixtures.replication')


    def wipe_dir(self, d):
        if os.path.isdir(d):
            shutil.rmtree(d)


    def __enter__(self):
        self.wipe_dir(self.fixtures)
        self.wipe_dir(self.fixtures_replication)
        tar = tarfile.open(filename('fixtures.tar.gz'), 'r:gz')
        tar.extractall(this_dir)

        st, outp = commands.getstatusoutput('cp -R %s %s' % (
                self.fixtures, self.fixtures_replication))
        if st != 0:
            msg = 'Error copying fixtures: \n%s\n\nreturn code: %s' % (outp, st)
            raise AssertionError(msg)

        return self


    def __exit__(self, *args, **kwargs):
        pass
    



class MongoDB(ProcessController):
    def __init__(self, port, name, dbpath):
        ProcessController.__init__(self, port, name)
        self.dbpath = dbpath

    def get_command(self):
        return [self.find_executable('mongod'), '--dbpath='+self.dbpath, 
                '--nohttpinterface', '--port=%s' % self.port]



class MongoDBRecovery(MongoDB):
    def __init__(self, fixture_data):
        MongoDB.__init__(self, settings.MONGOD_PORT, 'mongod.recovery', 
                         fixture_data.fixtures)




class MongoDBReplicationOptions(MongoDB):
    def __init__(self, fixture_data):
        MongoDB.__init__(self, settings.MONGOD_REPLICATION_PORT, 
                         'mongod.replication', fixture_data.fixtures_replication)


    def get_command(self):
        return MongoDB.get_command(self) + ['--master']



class TestSuite(unittest.TestSuite):
    def run(self, result):
        with FixtureData() as d:
            with MongoDBRecovery(d):
                with MongoDBReplicationOptions(d):
                    return unittest.TestSuite.run(self, result)



class TestLoader(ScanningLoader):
    def loadTestsFromNames(self, *args, **kwargs):
        s = ScanningLoader.loadTestsFromNames(self, *args, **kwargs)
        wrapper = TestSuite()
        wrapper.addTests(s)
        return wrapper

    
