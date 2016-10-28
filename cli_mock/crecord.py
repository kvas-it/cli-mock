from __future__ import unicode_literals

import argparse
import io
import subprocess
import sys
import threading


def forward_stream(stream, out, log, prefix):
    """Forward stream to output stream prefixing lines with prefix."""

    def forward():
        for line in stream:
            out.write(line)
            if line.endswith('\n'):
                template = '{} {}'
            else:
                template = '{}|{}\n'
            log.write(template.format(prefix, line))

    thread = threading.Thread(target=forward)
    thread.daemon = True
    thread.start()
    return thread


def main():
    parser = argparse.ArgumentParser(
        description='Log output of command line utilities'
    )
    parser.add_argument('-l', '--log', default='log.txt', help='log file')
    parser.add_argument('cmd', nargs='+', help='command and options')
    args = parser.parse_args()
    with io.open(args.log, 'a', encoding='utf-8') as log:
        log.write('$ {}\n'.format(' '.join(args.cmd)))
        proc = subprocess.Popen(args.cmd,
                                stdout=subprocess.PIPE,
                                stderr=subprocess.PIPE,
                                universal_newlines=True)
        out_watcher = forward_stream(proc.stdout, sys.stdout, log, '>')
        err_watcher = forward_stream(proc.stderr, sys.stderr, log, '!')
        proc.wait()
        out_watcher.join()
        err_watcher.join()
        log.write('= {}\n'.format(proc.returncode))
        sys.exit(proc.returncode)
