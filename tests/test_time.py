import os
import time
from datetime import UTC, datetime
from unittest.mock import patch

import pytest

from handy.commands.time import time_cmd


@pytest.fixture(autouse=True)
def _fixed_timezone():
    """Lock timezone to Asia/Shanghai for all tests in this file."""
    original_tz = os.environ.get("TZ")
    os.environ["TZ"] = "Asia/Shanghai"
    time.tzset()
    try:
        yield
    finally:
        if original_tz is not None:
            os.environ["TZ"] = original_tz
        else:
            os.environ.pop("TZ", None)
        time.tzset()


def test_base_parse_time(cli):
    result = cli(time_cmd, ["1714339200"])
    assert result.exit_code == 0
    lines = [line.strip() for line in result.output.strip().split("\n")]
    assert "ts     1714339200" in lines
    assert "space  2024-04-29 05:20:00" in lines


def test_millisecond_time(cli):
    result = cli(time_cmd, ["1714339200.123"])
    assert result.exit_code == 0
    lines = [line.strip() for line in result.output.strip().split("\n")]
    assert "ts     1714339200           1714339200.123" in lines
    assert "space  2024-04-29 05:20:00  2024-04-29 05:20:00.123" in lines

    result = cli(time_cmd, ["1714339200123"])
    assert result.exit_code == 0
    lines = [line.strip() for line in result.output.strip().split("\n")]
    assert "ts     1714339200           1714339200.123" in lines
    assert "space  2024-04-29 05:20:00  2024-04-29 05:20:00.123" in lines


@patch("handy.commands.time.datetime", wraps=datetime)
def test_now_time(mock_datetime, cli):
    fixed_now = datetime(2024, 4, 29, 13, 20, 0, tzinfo=UTC)
    mock_datetime.now.return_value = fixed_now

    empty_now = cli(time_cmd, [])
    assert empty_now.exit_code == 0
    assert "ts     1714396800" in empty_now.output
    assert "space  2024-04-29 21:20:00" in empty_now.output

    now = cli(time_cmd, ["now"])
    assert now.exit_code == 0
    assert "ts     1714396800" in now.output

    assert empty_now.output == now.output


def test_input_iso_format(cli):
    result = cli(time_cmd, ["2024-04-29T21:20:00+08:00", "--iso"])
    assert result.exit_code == 0
    lines = [line.strip() for line in result.output.strip().split("\n")]
    assert "ts     1714396800" in lines
    assert "space  2024-04-29 21:20:00" in lines
    assert "T      2024-04-29T21:20:00+08:00" in lines

    # input without timezone
    result = cli(time_cmd, ["2024-04-29T13:20:00", "--iso"])
    assert result.exit_code == 0
    lines = [line.strip() for line in result.output.strip().split("\n")]
    assert "ts     1714396800" in lines
    assert "space  2024-04-29 21:20:00" in lines
    assert "T      2024-04-29T21:20:00+08:00" in lines

    # input with milliseconds
    result = cli(time_cmd, ["2024-04-29T13:20:00.123", "--iso"])
    assert result.exit_code == 0
    lines = [line.strip() for line in result.output.strip().split("\n")]
    assert "ts     1714396800                 1714396800.123" in lines
    assert "space  2024-04-29 21:20:00        2024-04-29 21:20:00.123" in lines
    assert "T      2024-04-29T21:20:00+08:00  2024-04-29T21:20:00.123+08:00" in lines
