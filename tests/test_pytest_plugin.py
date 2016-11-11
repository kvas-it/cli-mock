import subprocess

import pytest


@pytest.fixture(autouse=True)
def pc(popen_controller, testlog):
    popen_controller.set_replay_log(testlog.strpath)
    return popen_controller


def test_popen():
    proc = subprocess.Popen(['foo'], stdout=subprocess.PIPE,
                            stderr=subprocess.PIPE,
                            universal_newlines=True)
    retcode = proc.wait()
    assert retcode == 0
    assert proc.stdout.read() == 'foo\nbaz\n'
    assert proc.stderr.read() == 'bar\n'


def test_popen_error():
    proc = subprocess.Popen(['foo', 'bar'])
    assert proc.wait() == 1


def test_high_level_api():
    output = subprocess.check_output(['foo'], universal_newlines=True)
    assert output == 'foo\nbaz\n'
