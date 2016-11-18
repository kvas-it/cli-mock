def test_default_log(creplay, testlog):
    ret = creplay('echo', 'foo', creplay_args=[], cwd=testlog.dirname)
    assert ret.success
    assert ret.stdout == 'foo\n'
    assert ret.stderr == ''


def test_echo_n(creplay, logfile):
    ret = creplay('echo', '-n', 'foo')
    assert ret.success
    assert ret.stdout == 'foo'
    assert ret.stderr == ''


def test_err(creplay, logfile):
    ret = creplay('foo', 'bar')
    assert not ret.success
    assert ret.stdout == ''
    assert ret.stderr == 'Error\n'


def test_order(creplay, tmpdir, logfile):
    ret = creplay('./script.py')
    assert ret.success
    assert ret.stdout == 'foo\n123baz\n'
    assert ret.stderr == 'bar\n'


def test_record_replay(crecord, tmpdir, logfile, testlog):
    ret = crecord('creplay', '-l', testlog.strpath, 'foo')
    assert ret.success
    assert ret.stdout == 'foo\nbaz\n'
    assert ret.stderr == 'bar\n'
    lines = set(logfile.read().split('\n')[1:-1])
    # Unfortunately the order can get messed up.
    assert lines == {'> foo', '! bar', '> baz', '= 0'}
