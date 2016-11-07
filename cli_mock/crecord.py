from __future__ import unicode_literals

import argparse
import asyncio
import io
import locale
import sys


class LoggingProtocol(asyncio.SubprocessProtocol):
    """Asyncio protocol for running the process."""

    def __init__(self, log, retcode_future):
        self.log = log
        self.retcode_future = retcode_future

    def connection_made(self, transport):
        self.transport = transport

    def connection_lost(self, exc):
        self.retcode_future.set_result(self.transport.get_returncode())

    def pipe_data_received(self, fd, data):
        text = data.decode(locale.getpreferredencoding(False))

        if fd == 1:
            prefix, outstream = '>', sys.stdout
        else:  # 2
            prefix, outstream = '!', sys.stderr

        outstream.write(text)

        lines = text.split('\n')
        lines[:-1] = ['{} {}\n'.format(prefix, l) for l in lines[:-1]]
        if lines[-1] == '':
            lines.pop()
        else:
            lines[-1] = '{}|{}\n'.format(prefix, lines[-1])

        for line in lines:
            self.log.write(line)


@asyncio.coroutine
def log_exec(cmd, log, loop):
    log.write('$ {}\n'.format(' '.join(cmd)))
    retcode_future = asyncio.Future(loop=loop)
    transport, proto = yield from loop.subprocess_exec(
        lambda: LoggingProtocol(log, retcode_future),
        *cmd,
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE
    )
    retcode = yield from retcode_future
    log.write('= {}\n'.format(retcode))
    return retcode


def main():
    parser = argparse.ArgumentParser(
        description='Log output of command line utilities'
    )
    parser.add_argument('-l', '--log', default='log.txt', help='log file')
    parser.add_argument('cmd', nargs='+', help='command and options')
    args = parser.parse_args()
    with io.open(args.log, 'a', encoding='utf-8') as log:
        loop = asyncio.SelectorEventLoop()
        asyncio.set_event_loop(loop)
        try:
            sys.exit(loop.run_until_complete(log_exec(args.cmd, log, loop)))
        finally:
            loop.close()
