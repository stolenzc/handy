import base64

import click


@click.command()
@click.argument("original_str")
@click.option("--decode", "-d", is_flag=True, help="Decode the string.")
@click.option("--encode", "-e", is_flag=True, help="Encode the string(default option).")
def base64_cmd(original_str: str, decode: bool, encode: bool):
    """Base64 encode or decode a string."""
    if decode:
        result = base64.b64decode(original_str.encode("utf-8")).decode("utf-8")
    else:
        result = base64.b64encode(original_str.encode("utf-8")).decode("utf-8")
    click.echo(result)
