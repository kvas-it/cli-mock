import subprocess
import sys
import threading

import click


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


@click.command()
@click.option('-o', '--output', type=click.File('a'), help='Output file')
@click.argument('command', nargs=-1)
def main(output, command):
    output.write('$ {}\n'.format(' '.join(command)))
    proc = subprocess.Popen(command,
                            stdout=subprocess.PIPE,
                            stderr=subprocess.PIPE,
                            universal_newlines=True)
    out_watcher = forward_stream(proc.stdout, sys.stdout, output, '>')
    err_watcher = forward_stream(proc.stderr, sys.stderr, output, '!')
    proc.wait()
    out_watcher.join()
    err_watcher.join()
    output.write('= {}\n'.format(proc.returncode))
    sys.exit(proc.returncode)
