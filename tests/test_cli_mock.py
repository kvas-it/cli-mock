import pytest


@pytest.fixture()
def logfile(tmpdir):
    return tmpdir.join('log.txt')


def test_default_log(script_runner, tmpdir, logfile):
    ret = script_runner.run('crecord', 'echo', 'foo', cwd=str(tmpdir))
    assert ret.success
    assert ret.stdout == 'foo\n'
    assert ret.stderr == ''
    assert logfile.read() == '$ echo foo\n> foo\n= 0\n'


@pytest.fixture()
def crecord(script_runner, tmpdir, logfile):
    def crecord(*args, **kw):
        ret = script_runner.run('crecord', '-l', str(logfile), '--',
                                cwd=str(tmpdir), *args, **kw)
        print(ret.stderr)
        return ret
    return crecord


def test_crecord_echo(crecord, logfile):
    ret = crecord('echo', 'foo')
    assert ret.success
    assert ret.stdout == 'foo\n'
    assert ret.stderr == ''
    assert logfile.read() == '$ echo foo\n> foo\n= 0\n'


# def test_crecord_echo_n(crecord, logfile):
#     ret = crecord('echo', '-n', 'foo')
#     assert ret.success
#     assert ret.stdout == 'foo'
#     assert ret.stderr == ''
#     assert logfile.read() == '$ echo -n foo\n>|foo\n= 0\n'


# def test_crecord_err(crecord, logfile):
#     ret = crecord('ls', 'foo')
#     assert not ret.success
#     assert ret.stdout == ''
#     assert 'foo' in ret.stderr
#     assert logfile.read() == '$ ls foo\n! {}= 1\n'.format(ret.stderr)


# def test_crecord_order(crecord, tmpdir, logfile):
#     script = tmpdir.join('script.sh')
#     script.write("""#!/bin/sh
# echo foo
# sleep 0.01  # Sleep to defeat the scheduler.
# echo bar >&2
# sleep 0.01
# echo baz
#     """)
#     script.chmod(0o777)
#     ret = crecord('./script.sh')
#     assert ret.success
#     assert ret.stdout == 'foo\nbaz\n'
#     assert ret.stderr == 'bar\n'
#     print(logfile.read())
#     assert logfile.read() == '$ ./script.sh\n> foo\n! bar\n> baz\n= 0\n'
