import pytest


@pytest.fixture()
def logfile(tmpdir):
    return tmpdir.join('log.txt')
