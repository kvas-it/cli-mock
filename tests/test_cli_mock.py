def test_crecord(script_runner):
    ret = script_runner.run('crecord')
    assert ret.success
    assert ret.stdout == 'Record\n'
    assert ret.stderr == ''


def test_creplay(script_runner):
    ret = script_runner.run('creplay')
    assert ret.success
    assert ret.stdout == 'Replay\n'
    assert ret.stderr == ''
