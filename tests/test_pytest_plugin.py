import subprocess

import pytest


@pytest.fixture()
def pc(popen_controller, testlog):
    popen_controller.set_replay_log(testlog.strpath)
    return popen_controller


def test_popen(pc):
    proc = subprocess.Popen(['foo'], stdout=subprocess.PIPE,
                            stderr=subprocess.PIPE,
                            universal_newlines=True)
    retcode = proc.wait()
    assert retcode == 0
    assert proc.stdout.read() == 'foo\nbaz\n'
    assert proc.stderr.read() == 'bar\n'


def test_popen_error(pc):
    proc = subprocess.Popen(['foo', 'bar'])
    assert proc.wait() == 1


def test_high_level_api(pc):
    output = subprocess.check_output(['foo'], universal_newlines=True)
    assert output == 'foo\nbaz\n'


def test_strictness(pc):
    """The code is not allwed to run commands not in the log."""
    with pytest.raises(AssertionError) as raised:
        subprocess.Popen(['ls', 'foo'])
    assert str(raised.value) == 'Unexpected command: ls foo'


def test_non_strict(pc, testlog):
    pc.set_replay_log(testlog.strpath, strict=False)
    proc = subprocess.Popen(['true'])
    assert proc.wait() == 0


def test_set_strict(pc):
    pc.set_strict(False)
    proc = subprocess.Popen(['true'])
    assert proc.wait() == 0
    pc.set_strict(True)
    with pytest.raises(AssertionError):
        subprocess.Popen(['true'])
