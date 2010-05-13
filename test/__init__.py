from __future__ import with_statement
import os
from setuptools.command.test import ScanningLoader
import unittest
import commands
import subprocess
from util import ProcessController
import settings
from pymongo import Connection
import shutil

this_dir = os.path.realpath(os.path.dirname(__file__))



class MongoDB(ProcessController):
    def __init__(self):
        ProcessController.__init__(self, settings.MONGOD_PORT, 'mongod')
        self.dbpath = os.path.join(this_dir, '.mongodb')


    def get_command(self):
        return [self.find_executable('mongod'), '--master', 
                '--oplogSize=10', '--dbpath='+self.dbpath, 
                '--port=%s' % self.port]


    def wipe_data_dir(self):
        if os.path.isdir(self.dbpath):
            shutil.rmtree(self.dbpath)
        os.mkdir(self.dbpath)


    def load_fixtures(self):
        c = Connection('localhost', self.port)
        c.testdb.test.insert({ 'foo': 1, 'bar': 2 })
        c.testdb.test.insert({ 'foo': 2, 'bar': 2 })
        c.testdb.test.insert({ 'foo': 3, 'bar': 2 })


class TestSuite(unittest.TestSuite):
    def run(self, result):
        mongo = MongoDB()
        mongo.wipe_data_dir()
        with mongo:
            mongo.load_fixtures()
            return unittest.TestSuite.run(self, result)



class TestLoader(ScanningLoader):
    def loadTestsFromNames(self, *args, **kwargs):
        s = ScanningLoader.loadTestsFromNames(self, *args, **kwargs)
        wrapper = TestSuite()
        wrapper.addTests(s)
        return wrapper

    
