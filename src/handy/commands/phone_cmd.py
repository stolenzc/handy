import click
from phonenumbers import carrier, geocoder, is_valid_number, parse


@click.command()
@click.argument("phone")
@click.option(
    "--lang",
    "-l",
    type=click.Choice(["zh", "en"]),
    default="zh",
    help="Language for display detail.",
)
def phone_cmd(phone, lang):
    """
    Parse phone number and display detailed information.
    """
    if phone.startswith("+"):
        region = None
    else:
        region = "CN"
    phone_number = parse(phone, region=region)
    click.echo("Valid: " + str(is_valid_number(phone_number)))
    click.echo("Country: " + geocoder.country_name_for_number(phone_number, lang))
    click.echo("Location: " + geocoder.description_for_number(phone_number, lang))
    click.echo("Carrier: " + carrier.name_for_number(phone_number, lang))
