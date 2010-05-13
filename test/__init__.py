from setuptools.command.test import ScanningLoader
import unittest



class TestSuite(unittest.TestSuite):

    def run(self, result):
        self.suiteSetup()
        try:
            return unittest.TestSuite.run(self, result)
        finally:
            self.suiteTeardown()


    def suiteSetup(self):
        pass


    def suiteTeardown(self):
        pass



class TestLoader(ScanningLoader):
    def loadTestsFromNames(self, *args, **kwargs):
        s = ScanningLoader.loadTestsFromNames(self, *args, **kwargs)
        wrapper = TestSuite()
        wrapper.addTests(s)
        return wrapper

    
