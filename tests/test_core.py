"""Tests for calendar_grid_layout.core."""

import calendar
import unittest

from calendar_grid_layout import render_month, CalendarConfig


class TestRenderMonth(unittest.TestCase):
    def test_february_2024_leap_has_five_week_rows(self):
        result = render_month(2024, 2)
        lines = result.split("\n")
        self.assertEqual(len(lines), 6)  # header + 5 week rows

    def test_february_2025_non_leap_has_five_week_rows(self):
        result = render_month(2025, 2)
        lines = result.split("\n")
        self.assertEqual(len(lines), 6)  # header + 5 week rows

    def test_header_uses_three_letter_abbreviations(self):
        result = render_month(2024, 2)
        header = result.split("\n")[0].strip()
        self.assertEqual(header, "Mon Tue Wed Thu Fri Sat Sun")

    def test_first_row_blank_cells_leading(self):
        # Feb 2024 starts on Thursday (Mon=0). Mon, Tue, Wed are blank.
        result = render_month(2024, 2)
        first_week_line = result.split("\n")[1]
        # With cell_width=4, left_pad=1, three blank cells (4 spaces each = 12)
        # plus 1 left_pad = 13 spaces, then day "1" right-aligned in 4 chars
        # ("   1" — 3 spaces + digit) adds 3 more spaces, total 16 before "1".
        self.assertTrue(first_week_line.startswith("                1"))

    def test_last_day_29_appears(self):
        result = render_month(2024, 2)
        self.assertIn("29", result)

    def test_non_leap_february_has_no_29(self):
        result = render_month(2025, 2)
        self.assertNotIn("29", result)

    def test_trailing_blank_cells_padded(self):
        # Feb 2025 ends on Friday Feb 28. Sat, Sun should be blank.
        result = render_month(2025, 2)
        week_lines = result.split("\n")[1:]
        last_week = week_lines[-1]
        self.assertTrue(last_week.rstrip().endswith("28"))

    def test_days_outside_month_replaced_with_spaces_not_dates(self):
        # Leading cells from January should not show Jan dates like 29,30,31.
        result = render_month(2024, 2)
        first_week_line = result.split("\n")[1]
        self.assertNotIn("31", first_week_line)
        self.assertNotIn("30", first_week_line)
        self.assertNotIn("29", first_week_line)

    def test_invalid_month_raises(self):
        with self.assertRaises(ValueError):
            render_month(2024, 0)
        with self.assertRaises(ValueError):
            render_month(2024, 13)

    def test_default_config_cell_width_is_four(self):
        # With cell_width=4 and left_pad=1, header line starts with one space
        # then the first cell " Mon" (right-aligned in 4 chars).
        result = render_month(2024, 2)
        header = result.split("\n")[0]
        self.assertEqual(header[0], " ")
        self.assertEqual(header[1:5], " Mon")

    def test_custom_config_wider_cells(self):
        config = CalendarConfig(cell_width=6, left_pad=0)
        result = render_month(2024, 2, config=config)
        header = result.split("\n")[0]
        self.assertEqual(header, "   Mon   Tue   Wed   Thu   Fri   Sat   Sun")

    def test_invalid_cell_width_raises(self):
        with self.assertRaises(ValueError):
            CalendarConfig(cell_width=2)

    def test_output_has_no_blank_lines_between_weeks(self):
        result = render_month(2024, 2)
        lines = result.split("\n")
        for line in lines[1:]:
            self.assertTrue(len(line) > 0)

    def test_january_2024_starts_on_monday_no_leading_blanks(self):
        result = render_month(2024, 1)
        first_week_line = result.split("\n")[1]
        # January 1, 2024 is a Monday. So first cell is "  1".
        stripped = first_week_line.lstrip()
        self.assertTrue(stripped.startswith("1"))

    def test_header_matches_calendar_day_abbr(self):
        result = render_month(2024, 2)
        header = result.split("\n")[0].strip()
        expected = " ".join(calendar.day_abbr[i] for i in range(7))
        self.assertEqual(header, expected)


if __name__ == "__main__":
    unittest.main()
