import click

from handy.commands.decrypt import decrypt
from handy.commands.dict_convert import dict_cmd
from handy.commands.time import time as time_cmd
from handy.commands.version import version


@click.group()
def cli():
    """Handy CLI tools."""
    pass


cli.add_command(decrypt)
cli.add_command(time_cmd)
cli.add_command(dict_cmd)
cli.add_command(version)


def main():
    cli()
