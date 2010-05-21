# oplogutils - Utilities for inspecting and manipulating the MongoDB oplog

## Overview

This package contains utilities for manipulating a MongoDB oplog, which can be
necessary in recovery scenarios. The tools are:

<pre>
oplog-count - counts the number of events in the oplog after a certain date 
              and time.
oplog-trim  - deletes events from the oplog after a certain date and time.
</pre>


## Installation

To install from source, extract the tarball and use the following commands.

<pre>
python setup.py build
sudo python setup.py install
</pre>


## Unit Tests

oplogutils comes with a fairly complete unit test suite. The suite requires the
`mongod` program to be somewhere in the `$PATH`. To run the tests, use:

> python setup.py test

## Version History

### Version 0.1 
05-21-2010 - Initial release

