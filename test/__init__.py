from __future__ import with_statement
from contextlib import contextmanager, nested
import os
from setuptools.command.test import ScanningLoader
import unittest
import commands
from util import MongoDB, FixtureData, FixtureCopy
import settings
from pymongo import Connection



def MongoDBRecovery(dbpath):
    return MongoDB(settings.MONGOD_PORT, 'mongod.recovery', dbpath)


class MongoDBReplicationOptions(MongoDB):
    def __init__(self, dbpath):
        MongoDB.__init__(self, settings.MONGOD_REPLICATION_PORT, 
                         'mongod.replication', dbpath)

    def get_command(self):
        return MongoDB.get_command(self) + ['--master']



class TestSuite(unittest.TestSuite):
    def run(self, result):
        with nested(FixtureData(), FixtureCopy('fixtures.1'), 
                    FixtureCopy(settings.FIXTURES_COPY)) as (d, c1, c2):
            with nested(MongoDBRecovery(d), MongoDBReplicationOptions(c1)):
                return unittest.TestSuite.run(self, result)



class TestLoader(ScanningLoader):
    def loadTestsFromNames(self, *args, **kwargs):
        s = ScanningLoader.loadTestsFromNames(self, *args, **kwargs)
        wrapper = TestSuite()
        wrapper.addTests(s)
        return wrapper

