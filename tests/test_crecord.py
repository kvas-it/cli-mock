def test_default_log(script_runner, tmpdir, logfile):
    ret = script_runner.run('crecord', 'echo', 'foo', cwd=str(tmpdir))
    assert ret.success
    assert ret.stdout == 'foo\n'
    assert ret.stderr == ''
    assert logfile.read() == '$ echo foo\n> foo\n= 0\n'


def test_echo(crecord, logfile):
    ret = crecord('echo', 'foo')
    assert ret.success
    assert ret.stdout == 'foo\n'
    assert ret.stderr == ''
    assert logfile.read() == '$ echo foo\n> foo\n= 0\n'


def test_echo_n(crecord, logfile):
    ret = crecord('echo', '-n', 'foo')
    assert ret.success
    assert ret.stdout == 'foo'
    assert ret.stderr == ''
    assert logfile.read() == '$ echo -n foo\n>|foo\n= 0\n'


def test_err(crecord, pyscript, logfile):
    pyscript.write("""#!/usr/bin/env python
import sys
sys.stderr.write('error\\n')
sys.exit(1)
    """)
    ret = crecord('./script.py')
    assert not ret.success
    assert ret.stdout == ''
    assert ret.stderr == 'error\n'
    assert logfile.read() == '$ ./script.py\n! error\n= 1\n'


def test_order(crecord, pyscript, logfile):
    pyscript.write("""#!/usr/bin/env python
import sys, time
sys.stdout.write('foo\\n123')
sys.stdout.flush()
time.sleep(0.001)
sys.stderr.write('bar\\n')
sys.stderr.flush()
time.sleep(0.001)
sys.stdout.write('baz\\n')
    """)
    ret = crecord('./script.py')
    assert ret.success
    assert ret.stdout == 'foo\n123baz\n'
    assert ret.stderr == 'bar\n'
    assert logfile.read() == '$ ./script.py\n> foo\n>|123\n! bar\n> baz\n= 0\n'
