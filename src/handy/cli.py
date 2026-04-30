import click

from handy.commands.base64_cmd import base64_cmd
from handy.commands.completion import completion
from handy.commands.decrypt import decrypt_cmd
from handy.commands.dict_convert import dict_cmd
from handy.commands.time import time_cmd
from handy.commands.url_cmd import url_cmd
from handy.commands.version import version


@click.group()
def cli():
    """Handy CLI tools."""
    pass


cli.add_command(base64_cmd)
cli.add_command(completion)
cli.add_command(decrypt_cmd)
cli.add_command(dict_cmd)
cli.add_command(time_cmd)
cli.add_command(url_cmd)
cli.add_command(version)


def main():
    cli()
