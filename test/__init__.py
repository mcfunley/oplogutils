from __future__ import with_statement
import os
from setuptools.command.test import ScanningLoader
import unittest
import commands
import subprocess
from util import ProcessController
import settings

this_dir = os.path.realpath(os.path.dirname(__file__))



class MongoDB(ProcessController):
    def __init__(self):
        ProcessController.__init__(self, settings.MONGOD_PORT, 'mongod')
        self.dbpath = os.path.join(this_dir, '.mongodb')


    def get_command(self):
        return [self.find_executable('mongod'), '--master', 
                '--oplogSize=10', '--dbpath='+self.dbpath, 
                '--port=%s' % self.port]


    def ensure_data_dir(self):
        if not os.path.isdir(self.dbpath):
            os.mkdir(self.dbpath)



class TestSuite(unittest.TestSuite):
    def run(self, result):
        mongo = MongoDB()
        mongo.ensure_data_dir()
        with mongo:
            return unittest.TestSuite.run(self, result)



class TestLoader(ScanningLoader):
    def loadTestsFromNames(self, *args, **kwargs):
        s = ScanningLoader.loadTestsFromNames(self, *args, **kwargs)
        wrapper = TestSuite()
        wrapper.addTests(s)
        return wrapper

    
