Cli Mock
========

.. image:: https://travis-ci.org/kvas-it/pytest-console-scripts.svg?branch=master
    :target: https://travis-ci.org/kvas-it/pytest-console-scripts
    :alt: See Build Status on Travis CI

This package provides two command line utilities: ``crecord`` and ``creplay``.
The former records the output (stdout and stderr) and the return code of a
command and the latter replays the command invocation by reproducing its output
and return code::

    $ crecord echo foo
    foo
    $ creplay echo foo
    foo
    $ crecord ls foo
    ls: foo: No such file or directory
    $ creplay ls foo
    ls: foo: No such file or directory
    $ echo $?
    1

This could be used to mock slow and environment-dependent command invocations
for testing purposes.
