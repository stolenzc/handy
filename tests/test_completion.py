from handy.commands.completion import completion


def test_completion_zsh(cli):
    result = cli(completion, ["zsh"])
    assert result.exit_code == 0
    assert "#compdef handy" in result.output


def test_completion_bash(cli):
    result = cli(completion, ["bash"])
    assert result.exit_code == 0
    assert "_handy_completion()" in result.output


def test_completion_fish(cli):
    result = cli(completion, ["fish"])
    assert result.exit_code == 0
    assert "function _handy_completion" in result.output
