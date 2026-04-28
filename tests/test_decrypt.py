import base64
from unittest.mock import patch

import pytest
from Crypto.Cipher import PKCS1_v1_5
from Crypto.PublicKey import RSA

from handy.commands.decrypt import decrypt_cmd

encrypt_json_data = """{
    "a": 1,
    "b": 2
}"""


def _rsa_encrypt(plaintext: str, public_key) -> str:
    """Encrypt plaintext with the given public key, double-base64-encode the result."""
    cipher = PKCS1_v1_5.new(public_key)
    encrypted = cipher.encrypt(plaintext.encode())
    return base64.b64encode(base64.b64encode(encrypted)).decode()


@pytest.fixture(scope="module")
def rsa_key_pair():
    """Generate an RSA key pair once for the whole module."""
    key = RSA.generate(1024)
    return key.publickey(), key.export_key().decode()


@patch("handy.commands.decrypt.load_config")
def test_config_private_key(mock_load_config, cli, rsa_key_pair):
    public_key, private_key = rsa_key_pair
    en_data = _rsa_encrypt(encrypt_json_data, public_key)
    mock_load_config.return_value = {"private_key": private_key}

    result = cli(decrypt_cmd, [en_data])
    assert result.exit_code == 0
    assert result.output.strip() == encrypt_json_data


@patch("handy.commands.decrypt.load_config")
def test_config_private_key_file(mock_load_config, cli, rsa_key_pair, tmp_path):
    public_key, private_key = rsa_key_pair
    en_data = _rsa_encrypt(encrypt_json_data, public_key)
    key_file = tmp_path / "private.pem"
    key_file.write_text(private_key)
    mock_load_config.return_value = {"private_key_file": key_file}

    result = cli(decrypt_cmd, [en_data])
    assert result.exit_code == 0
    assert result.output.strip() == encrypt_json_data


@patch("handy.commands.decrypt.load_config")
def test_config_private_key_file_not_exists(
    mock_load_config,
    cli,
    rsa_key_pair,
    tmp_path,
):
    public_key, _ = rsa_key_pair
    en_data = _rsa_encrypt("hello", public_key)
    key_file = tmp_path / "private.pem"
    mock_load_config.return_value = {"private_key_file": key_file}

    result = cli(decrypt_cmd, [en_data])
    assert result.exit_code == 1
    assert "No private key configured." in result.output
    assert "'private_key' or 'private_key_file'" in result.output


def test_input_private_key(cli, rsa_key_pair):
    public_key, private_key = rsa_key_pair
    en_data = _rsa_encrypt(encrypt_json_data, public_key)

    result = cli(decrypt_cmd, [en_data, "--key", private_key])
    assert result.exit_code == 0
    assert result.output.strip() == encrypt_json_data


def test_input_private_key_file(cli, rsa_key_pair, tmp_path):
    public_key, private_key = rsa_key_pair
    en_data = _rsa_encrypt(encrypt_json_data, public_key)
    key_file = tmp_path / "private.pem"
    key_file.write_text(private_key)

    result = cli(decrypt_cmd, [en_data, "--key-file", str(key_file)])
    assert result.exit_code == 0
    assert result.output.strip() == encrypt_json_data


def test_encrypt_not_json(cli, rsa_key_pair):
    public_key, private_key = rsa_key_pair
    plaintext = "not json data"
    en_data = _rsa_encrypt(plaintext, public_key)

    result = cli(decrypt_cmd, [en_data, "--key", private_key])
    assert result.exit_code == 0
    assert result.output.strip() == plaintext
