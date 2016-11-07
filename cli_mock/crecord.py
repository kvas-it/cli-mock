from __future__ import unicode_literals

import argparse
import asyncio
import contextlib
import io
import locale
import sys


class LoggingProtocol(asyncio.SubprocessProtocol):
    """Asyncio protocol for running the process."""

    def __init__(self, loop, log):
        self.log = log
        self.loop = loop

    def process_exited(self):
        self.loop.stop()

    def pipe_data_received(self, fd, data):
        text = data.decode(locale.getpreferredencoding(False))
        if fd == 1:
            self.log.write('> ' + text)
            sys.stdout.write(text)
        elif fd == 2:
            self.log.write('! ' + text)
            sys.stderr.write(text)


def main():
    parser = argparse.ArgumentParser(
        description='Log output of command line utilities'
    )
    parser.add_argument('-l', '--log', default='log.txt', help='log file')
    parser.add_argument('cmd', nargs='+', help='command and options')
    args = parser.parse_args()

    log = io.open(args.log, 'a', encoding='utf-8')
    with log as log, contextlib.closing(asyncio.get_event_loop()) as loop:
        log.write('$ {}\n'.format(' '.join(args.cmd)))
        transport, _ = loop.run_until_complete(loop.subprocess_exec(
            lambda: LoggingProtocol(loop, log),
            *args.cmd,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE
        ))
        loop.run_forever()
        retcode = transport.get_returncode()
        log.write('= {}\n'.format(retcode))
        sys.exit(retcode)
