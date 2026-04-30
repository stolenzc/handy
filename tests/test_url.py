from handy.commands.url_cmd import url_cmd

ORIGINAL_URL = "https://www.google.com/search?q=hello+world"
ENCODED_URL = "https%3A%2F%2Fwww.google.com%2Fsearch%3Fq%3Dhello%2Bworld"


def test_url_encode(cli):
    result = cli(url_cmd, [ORIGINAL_URL])
    assert result.exit_code == 0
    assert result.output.strip() == ENCODED_URL

    result = cli(url_cmd, [ORIGINAL_URL, "-e"])
    assert result.exit_code == 0
    assert result.output.strip() == ENCODED_URL

    result = cli(url_cmd, [ORIGINAL_URL, "--encode"])
    assert result.exit_code == 0
    assert result.output.strip() == ENCODED_URL


def test_url_decode(cli):
    result = cli(url_cmd, [ENCODED_URL, "-d"])
    assert result.exit_code == 0
    assert result.output.strip() == ORIGINAL_URL

    result = cli(url_cmd, [ENCODED_URL, "--decode"])
    assert result.exit_code == 0
    assert result.output.strip() == ORIGINAL_URL
