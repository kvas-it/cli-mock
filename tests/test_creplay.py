import pytest


def test_default_log(script_runner, tmpdir, logfile):
    logfile.write('$ echo foo\n> foo\n= 0\n')
    ret = script_runner.run('creplay', 'echo', 'foo', cwd=str(tmpdir))
    assert ret.success
    assert ret.stdout == 'foo\n'
    assert ret.stderr == ''


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


@pytest.fixture
def logfile2(tmpdir):
    return tmpdir.join('log2.txt')


def test_record_replay(crecord, tmpdir, logfile, logfile2):
    logfile2.write('$ foo\n> foo\n! bar\n> baz\n= 0\n')
    ret = crecord('creplay', '-l', logfile2.strpath, 'foo')
    assert ret.success
    assert ret.stdout == 'foo\nbaz\n'
    assert ret.stderr == 'bar\n'
    lines = set(logfile.read().split('\n')[1:-1])
    # Unfortunately the order can get messed up.
    assert lines == {'> foo', '! bar', '> baz', '= 0'}
