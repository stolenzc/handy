from handy.commands.base64_cmd import base64_cmd

ENCODE_STR = "hello"
DECODE_STR = "aGVsbG8="


def test_encode(cli):
    result = cli(base64_cmd, [ENCODE_STR, "--encode"])
    assert result.exit_code == 0
    assert result.output.strip() == DECODE_STR

    # test optional arguments
    result = cli(base64_cmd, [ENCODE_STR])
    assert result.exit_code == 0
    assert result.output.strip() == DECODE_STR


def test_decode(cli):

    result = cli(base64_cmd, [DECODE_STR, "--decode"])
    assert result.exit_code == 0
    assert result.output.strip() == ENCODE_STR
