import click


@click.command()
@click.option('-j', '--journal', type=click.File('br'), help='Journal file')
@click.argument('command', nargs=-1)
def main(journal, command):
    pass
