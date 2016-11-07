from __future__ import unicode_literals

import argparse
import io
import selectors
import subprocess
import sys


def forward(instream, outstream, log, prefix):
    """Forward input to output prefixing lines with prefix."""
    data = instream.read()
    outstream.write(data)

    if data == '':
        instream.close()
        return

    items = data.split('\n')
    items[:-1] = ['{} {}\n'.format(prefix, i) for i in items[:-1]]
    if items[-1] != '':
        items[-1] = '{}|{}\n'.format(prefix, items[-1])
    else:
        items = items[:-1]

    for item in items:
        log.write(item)


def main():
    parser = argparse.ArgumentParser(
        description='Log output of command line utilities'
    )
    parser.add_argument('-l', '--log', default='log.txt', help='log file')
    parser.add_argument('cmd', nargs='+', help='command and options')
    args = parser.parse_args()
    with io.open(args.log, 'a', encoding='utf-8') as log:
        log.write('$ {}\n'.format(' '.join(args.cmd)))
        proc = subprocess.Popen(args.cmd, bufsize=0,
                                stdout=subprocess.PIPE,
                                stderr=subprocess.PIPE,
                                universal_newlines=True)

        sel = selectors.DefaultSelector()
        sel.register(proc.stdout, selectors.EVENT_READ, (sys.stdout, '>'))
        sel.register(proc.stderr, selectors.EVENT_READ, (sys.stderr, '!'))

        while not (proc.stdout.closed and proc.stderr.closed):
            selected = sel.select()
            for sk, _ in selected:
                instream = sk.fileobj
                outstream, prefix = sk.data
                forward(instream, outstream, log, prefix)

        proc.wait()
        log.write('= {}\n'.format(proc.returncode))
        sys.exit(proc.returncode)
