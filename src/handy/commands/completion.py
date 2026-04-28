import click


@click.command()
@click.argument(
    "shell",
    type=click.Choice(["bash", "zsh", "fish"]),
    required=True,
)
def completion(shell: str) -> None:
    """Print shell completion script for the given shell."""
    from click.shell_completion import get_completion_class

    from handy.cli import cli

    comp_cls = get_completion_class(shell)
    comp = comp_cls(cli, {}, "handy", f"_HANDY_COMPLETE")
    click.echo(comp.source())
