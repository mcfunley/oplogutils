# oplogutils  

Utilities for inspecting and manipulating the MongoDB oplog.

By Dan McKinley - dan@etsy.com - [http://mcfunley.com](http://mcfunley.com)


## Overview

This package contains utilities for manipulating a MongoDB oplog, which can be
necessary in recovery scenarios. The tools are:

<pre>
  oplog-count - counts the number of events in the oplog after a certain date 
                 and time.
  oplog-trim  - deletes events from the oplog after a certain date and time.
</pre>


## Installation

The easiest way to install is using [setuptools](http://pypi.python.org/pypi/setuptools).

<pre>
$ easy_install oplogutils
</pre>

To install from source, extract the tarball and use the following commands.

<pre>
 $ python setup.py build 
 $ sudo python setup.py install
</pre>


## Examples

<pre>
oplog-trim --host=myhost.domain.com --port=27017 --remove-after="2010-05-22 03:42:00"
</pre>


## Unit Tests

oplogutils comes with a fairly complete unit test suite. The suite requires the
mongod program to be somewhere in the $PATH. To run the tests, use:

<pre>
python setup.py test
</pre>


## See Also

* [The MongoDB website](http://www.mongodb.org/)
* See [articles tagged MongoDB on the Etsy developer blog](http://codeascraft.etsy.com/tag/mongodb/) for some use cases. 


## Version History

### Version 0.1
*  05-21-2010 - Initial release

