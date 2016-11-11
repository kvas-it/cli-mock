"""Pytest plugin that mocks subprocess.Popen."""

import subprocess

import pytest

from .creplay import load_log


class PopenController:
    """Controller for mocking subprocess.Popen."""

    # Path to the currently active replay log.
    log_path = ''

    # Set of commands supported by current replay log.
    commands = set()  # type: Set[str]

    real_popen = subprocess.Popen

    @classmethod
    def set_replay_log(cls, log_path):
        cls.log_path = log_path
        cls.commands = set(load_log(log_path))

    @classmethod
    def clear_replay_log(cls):
        cls.log_path = ''
        cls.commands = set()

    @classmethod
    def popen(cls, cmd, *args, **kw):
        cmd_str = ' '.join(cmd)
        if cmd_str in cls.commands:
            return cls.real_popen(['creplay', '-l', cls.log_path, '--'] + cmd,
                                  *args, **kw)
        else:
            return cls.real_popen(cmd, *args, **kw)


@pytest.fixture
def popen_controller(monkeypatch):
    """Controller for subprocess.Popen."""
    monkeypatch.setattr(subprocess, 'Popen', PopenController.popen)
    yield PopenController
    PopenController.clear_replay_log()
