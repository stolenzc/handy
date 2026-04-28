from datetime import UTC, datetime

import click


def _parse_input(value: str) -> datetime:
    """Parse either a Unix timestamp or an ISO8601 string, return in local tz."""
    try:
        ts = float(value)
        if ts > 1e12:
            ts /= 1000
        return datetime.fromtimestamp(ts).astimezone()
    except ValueError:
        pass
    s = value.replace("Z", "+00:00")
    dt = datetime.fromisoformat(s)
    if dt.tzinfo is None:
        dt = dt.replace(tzinfo=UTC)
    return dt.astimezone()


def _format_results(dt: datetime, iso: bool = False) -> list[str]:
    has_ms = dt.microsecond > 0

    base = dt.strftime("%Y-%m-%d %H:%M:%S")
    t_base = dt.strftime("%Y-%m-%dT%H:%M:%S")
    tz = dt.strftime("%z")
    tz_part = f"{tz[:3]}:{tz[3:]}" if tz else ""

    ts = dt.timestamp()

    ts_val1 = str(int(ts))
    space_val1 = base
    t_val1 = f"{t_base}{tz_part}"

    if has_ms:
        ts_val2 = f"{ts:.3f}"
        space_val2 = f"{base}.{dt.microsecond // 1000:03d}"
        t_val2 = f"{t_base}.{dt.microsecond // 1000:03d}{tz_part}"
    else:
        ts_val2 = ""
        space_val2 = ""
        t_val2 = ""

    if iso:
        col1_width = max(len(ts_val1), len(space_val1), len(t_val1))
    else:
        col1_width = max(len(ts_val1), len(space_val1))

    lines = []

    label = f"{'ts':<6}"
    row = f"{ts_val1:<{col1_width}}"
    if ts_val2:
        row += f"  {ts_val2}"
    lines.append(f"{label} {row}")

    label = f"{'space':<6}"
    row = f"{space_val1:<{col1_width}}"
    if space_val2:
        row += f"  {space_val2}"
    lines.append(f"{label} {row}")

    if iso:
        label = f"{'T':<6}"
        row = f"{t_val1:<{col1_width}}"
        if t_val2:
            row += f"  {t_val2}"
        lines.append(f"{label} {row}")

    return lines


def _build_output(dt: datetime, iso: bool = False) -> str:
    """Build the full output string for a datetime. Pure function for easy testing."""
    lines = _format_results(dt, iso)
    return "\n".join(lines)


@click.command()
@click.argument("value", required=False)
@click.option(
    "--iso",
    is_flag=True,
    help="Show ISO8601 format (T-separated with timezone). Example: 2001-01-01T00:00:00+08:00.",
)
def time_cmd(value, iso):
    """Parse a timestamp or date string. Defaults to current time.

    Accepts: Unix timestamps (s/ms), ISO8601, or "YYYY-MM-DD HH:MM:SS".
    Use 'now' or no argument for current time.
    """
    if not value or value.lower() == "now":
        dt = datetime.now().astimezone()
    else:
        dt = _parse_input(value)
    click.echo(_build_output(dt, iso), color=True)
