import click


@click.command()
@click.argument("dict_str")
@click.option("--postman", "-p", is_flag=True, help="Output as Postman params (key:value per line).")
def dict_cmd(dict_str, postman):
    """Convert a Python dict literal to URL query string or Postman params.

    Default: URL query string. Pass --postman for Postman format.

    Examples:
        handy dict "{'key1': 'value1', 'key2': 'value2'}"
        handy dict --postman "{'key1': 'value1', 'key2': 'value2'}"
    """
    import ast

    try:
        d = ast.literal_eval(dict_str)
    except (ValueError, SyntaxError) as e:
        raise click.ClickException(f"Failed to parse dict: {e}")

    if not isinstance(d, dict):
        raise click.ClickException("Input must be a dict literal.")

    if postman:
        for key, value in d.items():
            click.echo(f"{key}:{value}")
    else:
        from urllib.parse import urlencode

        click.echo(urlencode(d))
