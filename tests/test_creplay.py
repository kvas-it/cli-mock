import pytest


def test_default_log(script_runner, tmpdir, logfile):
    logfile.write('$ echo foo\n> foo\n= 0\n')
    ret = script_runner.run('creplay', 'echo', 'foo', cwd=str(tmpdir))
    assert ret.success
    assert ret.stdout == 'foo\n'
    assert ret.stderr == ''


@pytest.fixture()
def creplay(script_runner, tmpdir, logfile):
    def creplay(*args, **kw):
        return script_runner.run('creplay', '-l', str(logfile), '--',
                                 cwd=str(tmpdir), *args, **kw)
    return creplay


def test_echo_n(creplay, logfile):
    logfile.write('$ echo -n foo\n>|foo\n= 0\n')
    ret = creplay('echo', '-n', 'foo')
    assert ret.success
    assert ret.stdout == 'foo'
    assert ret.stderr == ''


def test_err(creplay, logfile):
    logfile.write('$ foo bar\n! Error\n= 1\n')
    ret = creplay('foo', 'bar')
    assert not ret.success
    assert ret.stdout == ''
    assert ret.stderr == 'Error\n'


def test_order(creplay, tmpdir, logfile):
    logfile.write('$ ./script.py\n> foo\n>|123\n! bar\n> baz\n= 0\n')
    ret = creplay('./script.py')
    assert ret.success
    assert ret.stdout == 'foo\n123baz\n'
    assert ret.stderr == 'bar\n'
