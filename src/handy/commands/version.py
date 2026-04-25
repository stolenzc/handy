import importlib.metadata

import click


@click.command()
def version():
    """Show version."""
    click.echo(importlib.metadata.version("handy"))
