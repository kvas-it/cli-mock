import pytest


@pytest.fixture()
def logfile(tmpdir):
    return tmpdir.join('log.txt')


@pytest.fixture()
def creplay(script_runner, tmpdir, logfile):
    def creplay(*args, **kw):
        return script_runner.run('creplay', '-l', str(logfile), '--',
                                 cwd=tmpdir.strpath, *args, **kw)
    return creplay


@pytest.fixture()
def crecord(script_runner, tmpdir, logfile):
    def crecord(*args, **kw):
        ret = script_runner.run('crecord', '-l', str(logfile), '--',
                                cwd=tmpdir.strpath, *args, **kw)
        print(logfile.read())  # For test debugging.
        return ret
    return crecord


@pytest.fixture()
def pyscript(tmpdir):
    script = tmpdir.join('script.py')
    script.write('')
    script.chmod(0o777)
    return script
