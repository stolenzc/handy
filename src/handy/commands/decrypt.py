import base64
from pathlib import Path

import click
import ujson
from Crypto.Cipher import PKCS1_v1_5
from Crypto.PublicKey import RSA

from handy.config import load_config

MAX_DECRYPT_SIZE = 128


def rsa_decrypt(en_data: str, private_key: str) -> str:
    key = RSA.importKey(private_key)
    cipher = PKCS1_v1_5.new(key)
    # Double base64 decode to match original script behavior
    raw = base64.b64decode(base64.b64decode(en_data))
    chunks = []
    for i in range(0, len(raw), MAX_DECRYPT_SIZE):
        chunks.append(cipher.decrypt(raw[i : i + MAX_DECRYPT_SIZE], b"RSA"))
    return b"".join(chunks).decode("utf-8")


def load_private_key(config: dict) -> str:
    key = config.get("private_key")
    if key:
        return key
    key_path = config.get("private_key_file")
    if key_path:
        path = Path(key_path)
        if path.is_file():
            return path.read_text().strip()
    raise click.ClickException(
        "No private key configured. Set 'private_key' or 'private_key_file' in config.json."
    )


@click.command()
@click.argument("encrypted")
@click.option("--key", "key_arg", help="Use this private key directly instead of config.")
@click.option("--key-file", "key_file", type=click.Path(exists=True), help="Path to a private key file.")
def decrypt(encrypted, key_arg, key_file):
    """Decrypt an RSA-encrypted base64 string."""
    if key_arg:
        private_key = key_arg
    elif key_file:
        private_key = Path(key_file).read_text().strip()
    else:
        config = load_config()
        private_key = load_private_key(config)

    result = rsa_decrypt(encrypted, private_key)
    try:
        parsed = ujson.loads(result)
        click.echo(ujson.dumps(parsed, indent=4, ensure_ascii=False))
    except (ujson.JSONDecodeError, ValueError):
        click.echo(result)
