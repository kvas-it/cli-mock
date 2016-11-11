from __future__ import unicode_literals

import argparse
import io
import itertools
import sys


def load_log(log_path):
    """Load the log file into a dict."""
    ret = {}
    cmd = output = None
    with io.open(log_path, 'r', encoding='utf-8') as log:
        for line in itertools.chain(log, ['$ ']):
            line = line.strip('\n')
            if line.startswith('$ '):
                if cmd is not None:
                    ret[cmd] = output
                cmd = line[2:]
                output = []
            elif line and line[0] in {'>', '!', '='}:
                output.append(line)
    return ret


def replay_log(log):
    """Replay recorded output from log."""
    for line in log:
        if line.startswith('= '):
            return int(line[2:])
        if line.startswith('>'):
            stream = sys.stdout
        elif line.startswith('!'):
            stream = sys.stderr
        if line[1] == ' ':
            line += '\n'
        stream.write(line[2:])
    return 0


def main():
    parser = argparse.ArgumentParser(
        description='Replay the output of command line utilities.',
        epilog='In order to supply flags starting with "-" or "--" to '
               'the replayed command, prefix the command with "--".'
    )
    parser.add_argument('-l', '--log', default='log.txt', help='log file')
    parser.add_argument('cmd', help='command to replay')
    parser.add_argument('opts', nargs='*', help='options to the command')
    args = parser.parse_args()
    log = load_log(args.log)
    cmd = ' '.join([args.cmd] + args.opts)
    try:
        cmd_log = log[cmd]
    except KeyError:
        sys.exit('Command not in the log: {}'.format(cmd))
    sys.exit(replay_log(cmd_log))
