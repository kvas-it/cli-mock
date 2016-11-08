import pytest


@pytest.fixture()
def logfile(tmpdir):
    return tmpdir.join('log.txt')


@pytest.fixture()
def creplay(script_runner, tmpdir, logfile):
    def creplay(*args, **kw):
        return script_runner.run('creplay', '-l', str(logfile), '--',
                                 cwd=str(tmpdir), *args, **kw)
    return creplay


@pytest.fixture()
def crecord(script_runner, tmpdir, logfile):
    def crecord(*args, **kw):
        return script_runner.run('crecord', '-l', str(logfile), '--',
                                 cwd=str(tmpdir), *args, **kw)
    return crecord
