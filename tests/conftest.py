import pytest
from click.testing import CliRunner

# Import all command modules so coverage tracks them even without dedicated tests.
from handy.commands.base64_cmd import base64_cmd  # noqa: F401
from handy.commands.completion import completion  # noqa: F401
from handy.commands.decrypt import decrypt_cmd  # noqa: F401
from handy.commands.dict_convert import dict_cmd  # noqa: F401
from handy.commands.time import time_cmd  # noqa: F401
from handy.commands.url_cmd import url_cmd  # noqa: F401
from handy.commands.version import version  # noqa: F401


@pytest.fixture()
def cli():
    """Click CliRunner, call with (command, args)."""
    runner = CliRunner()

    def run(cmd, args=None, **kwargs):
        return runner.invoke(cmd, args or [], **kwargs)

    return run
