from handy.commands.dict_convert import dict_cmd


def test_query_basic(cli):
    result = cli(dict_cmd, ["{'key1': 'value1', 'key2': 'value2'}"])
    assert result.exit_code == 0
    assert result.output.strip() == "key1=value1&key2=value2"


def test_query_with_chinese(cli):
    result = cli(dict_cmd, ["{'name': '测试'}"])
    assert result.exit_code == 0
    assert "name=" in result.output


def test_postman_basic(cli):
    result = cli(dict_cmd, ["--postman", "{'key1': 'value1', 'key2': 'value2'}"])
    assert result.exit_code == 0
    lines = result.output.strip().split("\n")
    assert "key1:value1" in lines
    assert "key2:value2" in lines


def test_postman_short_flag(cli):
    result = cli(dict_cmd, ["-p", "{'a': '1'}"])
    assert result.exit_code == 0
    assert result.output.strip() == "a:1"


def test_invalid_dict(cli):
    result = cli(dict_cmd, ["'[1, 2, 3]'"])
    assert result.exit_code != 0
    assert "must be a dict" in result.output


def test_invalid_syntax(cli):
    result = cli(dict_cmd, ["{'a': 'invalid dict}"])
    assert result.exit_code != 0
    assert "Failed to parse dict" in result.output
