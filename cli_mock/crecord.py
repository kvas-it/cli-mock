from __future__ import unicode_literals

import argparse
import io
import locale
import os
import subprocess
import sys
import threading


def forward_stream(stream, out, log, prefix):
    """Forward stream to output stream prefixing lines with prefix."""

    def forward():
        while True:
            data = stream.read1(1024)
            if not data:
                return
            text = data.decode(locale.getpreferredencoding(False))
            lines = text.split('\n')
            for line in lines[:-1]:
                out.write(line + '\n')
                log.write('{} {}\n'.format(prefix, line))
            if lines[-1]:
                out.write(lines[-1])
                log.write('{}|{}\n'.format(prefix, lines[-1]))

    thread = threading.Thread(target=forward)
    thread.daemon = True
    thread.start()
    return thread


def main():
    parser = argparse.ArgumentParser(
        description='Record the output of command line utilities.',
        epilog='In order to supply flags starting with "-" or "--" to '
               'the invoked command, prefix the command with "--".'
    )
    parser.add_argument('-l', '--log', default='log.txt', help='log file')
    parser.add_argument('-c', '--comment', default=None,
                        help='comment to place in the log')
    parser.add_argument('cmd', help='command to run')
    parser.add_argument('opts', nargs='*', help='options to the command')
    args = parser.parse_args()
    cmd = [args.cmd] + args.opts
    with io.open(args.log, 'a', encoding='utf-8') as log:
        stats = os.stat(args.log)
        if stats.st_size > 0:
            log.write('\n')
        if args.comment is not None:
            log.write('# {}\n'.format(args.comment))
        log.write('$ {}\n'.format(' '.join(cmd)))
        proc = subprocess.Popen(cmd,
                                stdout=subprocess.PIPE,
                                stderr=subprocess.PIPE)
        out_watcher = forward_stream(proc.stdout, sys.stdout, log, '>')
        err_watcher = forward_stream(proc.stderr, sys.stderr, log, '!')
        proc.wait()
        out_watcher.join()
        err_watcher.join()
        log.write('= {}\n'.format(proc.returncode))
        sys.exit(proc.returncode)
