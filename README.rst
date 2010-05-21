==========
oplogutils  
==========

:Description: Utilities for inspecting and manipulating the MongoDB oplog
:Author: Dan McKinley - dan@etsy.com - `http://mcfunley.com <http://mcfunley.com>`_


Overview
========

This package contains utilities for manipulating a MongoDB oplog, which can be
necessary in recovery scenarios. The tools are:

> oplog-count - counts the number of events in the oplog after a certain date 
>               and time.
> oplog-trim  - deletes events from the oplog after a certain date and time.



Installation
============

To install from source, extract the tarball and use the following commands.

> $ python setup.py build
> $ sudo python setup.py install


Examples
========

## Unit Tests

oplogutils comes with a fairly complete unit test suite. The suite requires the
``mongod`` program to be somewhere in the ``$PATH``. To run the tests, use:

> python setup.py test


See Also
========

* `The MongoDB website <http://www.mongodb.org>`_
* See `articles tagged MongoDB on the Etsy developer blog <http://codeascraft.etsy.com/tag/mongodb/>`_ for some use cases. 


Version History
===============

Version 0.1
-----------
*  05-21-2010 - Initial release

