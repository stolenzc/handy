import importlib.metadata

from handy.commands.version import version


def test_version(cli):
    result = cli(version, [])
    assert result.exit_code == 0
    assert result.output.strip() == f"{importlib.metadata.version('handy')}"
