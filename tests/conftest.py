import os

import py
import pytest


@pytest.fixture()
def logfile(tmpdir):
    return tmpdir.join('log.txt')


@pytest.fixture()
def testlog():
    datadir = py.path.local(os.path.dirname(__file__)).join('data')
    return datadir.join('log.txt')


@pytest.fixture()
def creplay(script_runner, tmpdir, testlog):
    def creplay(*args, **kw):
        if 'creplay_args' in kw:
            creplay_args = kw['creplay_args']
            del kw['creplay_args']
        else:
            creplay_args = ['-l', str(testlog)]
        creplay_args.extend(['--'] + list(args))
        if 'cwd' not in kw:
            kw['cwd'] = tmpdir.strpath
        return script_runner.run('creplay', *creplay_args, **kw)
    return creplay


@pytest.fixture()
def crecord(script_runner, tmpdir, logfile):
    def crecord(*args, **kw):
        if 'crecord_args' in kw:
            crecord_args = kw['crecord_args']
            del kw['crecord_args']
        else:
            crecord_args = ['-l', str(logfile)]
        crecord_args.extend(['--'] + list(args))
        if 'cwd' not in kw:
            kw['cwd'] = tmpdir.strpath
        ret = script_runner.run('crecord', *crecord_args, **kw)
        print(logfile.read())  # For test debugging.
        return ret
    return crecord


@pytest.fixture()
def pyscript(tmpdir):
    script = tmpdir.join('script.py')
    script.write('')
    script.chmod(0o777)
    return script
