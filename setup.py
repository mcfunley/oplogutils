#!/usr/bin/python
import os
from setuptools import setup

this_dir = os.path.realpath(os.path.dirname(__file__))

long_description = open(os.path.join(this_dir, 'README.md'), 'r').read()
script = os.path.join(this_dir, 'scripts/oplog-trim')

setup(
    name = 'oplogutils',
    version = '0.1.2',
    author = 'Dan McKinley',
    author_email = 'dan@etsy.com',
    description = 'A oplog editing utility for mongodb.',
    license = 'GPL v3', 
    keywords = 'mongodb oplog backup restore utility', 
    scripts = [script], 
    packages = ['oplogutils'],
    long_description = long_description,
    install_requires = 'pymongo >= 1.6',
    test_loader = 'test:TestLoader',
    test_suite = 'test'
    )
