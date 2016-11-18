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

Pytest plugin
-------------

There's also a pytest plugin contained in cli_mock package. It exposes
``popen_controller`` fixture that can be used to replay ``crecord`` logs in
response to ``subprocess.Popen`` invocations (and the APIs that call it under
the hood)::

    def test_foo(popen_controller):
        popen_controller.set_replay_log(my_log)
        output = subprocess.check_output(['foo'])
        assert output == b'bar\n'

After the replay log is activated calls to ``subprocess.Popen`` and friends
with the commands that are contained in the log will replay from the log.
Commands that are not in the log will trigger an ``AssertionError``.

Non-strict mode
~~~~~~~~~~~~~~~

It's possible to allow executing commands that are not in the log via
activating non-strict mode::

    popen_controller.set_strict(False)

or::

    popen_controller.set_replay_log(my_log, strict=False)

In non-strict mode any command that is not in the log will be passed to
``subprocess.Popen`` without modifications and will be executed in a usual
fashion.
