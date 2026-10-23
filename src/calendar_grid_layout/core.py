"""Render a month as a multi-line calendar grid string.

The grid always has seven columns (one per weekday). Days that belong to the
target month are shown as right-aligned two-digit numbers; days from the
preceding or following month are replaced with spaces so the grid stays aligned
without displaying misleading dates.
"""

import calendar
from dataclasses import dataclass


@dataclass(frozen=True)
class CalendarConfig:
    """Configuration controlling the visual shape of the grid.

    All sizes are in characters. Keeping this a frozen dataclass makes the
    rendering function pure: same input always yields same output.
    """

    cell_width: int = 4
    left_pad: int = 1

    def __post_init__(self) -> None:
        if self.cell_width < 3:
            raise ValueError("cell_width must be >= 3")
        if self.left_pad < 0:
            raise ValueError("left_pad must be >= 0")


def _format_header_cell(weekday: int, config: CalendarConfig) -> str:
    """Return the header cell for a given weekday index (0=Monday).

    calendar.day_name is locale-dependent, so we always read from it at render
    time. The abbreviations come from calendar.day_abbr which is mutable for
    locale support but defaults to English three-letter names.
    """
    name = calendar.day_abbr[weekday]
    return name.rjust(config.cell_width)


def _format_day_cell(day: int, config: CalendarConfig) -> str:
    """Return the cell text for a day number, right-aligned in cell_width."""
    return str(day).rjust(config.cell_width)


def _format_blank_cell(config: CalendarConfig) -> str:
    """Return a blank cell representing a day outside the target month."""
    return " " * config.cell_width


def _build_row(cells: list[str], config: CalendarConfig) -> str:
    """Join cell strings into a single grid row, applying left padding."""
    return " " * config.left_pad + "".join(cells)


def render_month(year: int, month: int, config: CalendarConfig | None = None) -> str:
    """Return a multi-line string representing a month calendar grid.

    The first line is the weekday header (Monday through Sunday, using
    calendar.day_abbr abbreviations). Subsequent lines are weeks, each with
    seven cells. Only days in the target month are shown; days from adjacent
    months that calendar.monthdatescalendar would otherwise expose are
    replaced with blank cells.

    Args:
        year: The Gregorian year, e.g. 2024.
        month: The month 1-12.
        config: Optional visual configuration. Defaults to a 4-char cell
            width and 1-char left padding.

    Returns:
        A string with a header line and one line per week, separated by "\n".

    Raises:
        ValueError: If month is not in 1..12.
    """
    if not 1 <= month <= 12:
        raise ValueError(f"month must be in 1..12, got {month}")

    if config is None:
        config = CalendarConfig()

    cal = calendar.Calendar(firstweekday=0)  # Monday-first
    weeks = cal.monthdatescalendar(year, month)

    lines: list[str] = []

    # Header row: weekday abbreviations for Monday..Sunday.
    header_cells = [_format_header_cell(i, config) for i in range(7)]
    lines.append(_build_row(header_cells, config))

    for week in weeks:
        cells: list[str] = []
        for date in week:
            if date.month != month:
                cells.append(_format_blank_cell(config))
            else:
                cells.append(_format_day_cell(date.day, config))
        lines.append(_build_row(cells, config))

    return "\n".join(lines)
