from urllib.parse import quote, unquote

import click


@click.command()
@click.argument("text")
@click.option("--decode", "-d", is_flag=True, help="Decode the string.")
@click.option("--encode", "-e", is_flag=True, help="Encode the string (default).")
def url_cmd(text: str, decode: bool, encode: bool):
    """URL percent-encode or decode a string."""
    if decode:
        result = unquote(text)
    else:
        result = quote(text, safe="")
    click.echo(result)
