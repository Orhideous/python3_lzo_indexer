python3_lzo_indexer
===================

.. image:: https://img.shields.io/pypi/pyversions/python3_lzo_indexer
    :target: https://pypi.python.org/pypi/python3_lzo_indexer
.. image:: https://img.shields.io/pypi/v/python3_lzo_indexer.svg
    :target: https://pypi.python.org/pypi/python3_lzo_indexer
.. image:: https://coveralls.io/repos/github/Orhideous/python3_lzo_indexer/badge.svg?branch=master
    :target: https://coveralls.io/github/Orhideous/python3_lzo_indexer?branch=master
.. image:: https://img.shields.io/travis/Orhideous/python3_lzo_indexer.svg
    :target: https://travis-ci.org/Orhideous/python3_lzo_indexer
.. image:: https://pyup.io/repos/github/Orhideous/python3_lzo_indexer/shield.svg
    :target: https://pyup.io/repos/github/Orhideous/python3_lzo_indexer/


Python library for indexing block offsets within LZO compressed files.
The implementation is largely based on that of the `Hadoop Library`_.
Index files are used to allow Hadoop to split a single file compressed
with LZO into several chunks for parallel processing.

Since LZO is a block based compression algorithm, we can split the file
along the lines of blocks and decompress each block on it’s own. The
index is a file containing byte offsets for each block in the original
LZO file.

This library is python3 fork of `python-lzo-indexer`_.


Example
-------

The python code below demonstrates how easy it is to index an LZO file.
This library also supports indexing a string, and a method to return the
individual block offsets should you need to create a file of your own
format.

.. code:: python

   import lzo_indexer

   with open("my-file.lzo", "r") as f, open("my-file.lzo.index", "rw") as index:
       lzo_indexer.index_lzo_file(f, index)

Command-line Utility
--------------------

This library also includes a utility for indexing multiple lzo files,
using the python indexer. This is a much faster alternative to the
command line utility built into the hadoop-lzo library as it avoids the
JVM.

::

    $ lzo_indexer --help

    Usage: lzo_indexer [OPTIONS] <files to index>

      Tool for indexing LZO compressed files

    Options:
      -t, --threads INTEGER  Processing threads count
      -e, --extension TEXT   Index file extension
      -f, --force            Force re-creation of an index even if it exists
      -h, --help             Show this message and exit.

Contributions
-------------

I welcome any contributions, though I request that any pull requests
come with test coverage.

.. _Hadoop Library: https://github.com/twitter/hadoop-lzo
.. _python-lzo-indexer: https://github.com/duedil-ltd/python-lzo-indexer
