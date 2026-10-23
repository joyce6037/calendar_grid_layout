# calendar_grid_layout

`calendar_grid_layout` returns a multi-line string representing a single month as a calendar grid. Days outside the target month are replaced with blank cells so the grid stays aligned without printing misleading adjacent-month dates.

## Usage

```python
from calendar_grid_layout import render_month, CalendarConfig

print(render_month(2024, 2))
#  Mon Tue Wed Thu Fri Sat Sun
#            1   2   3   4
#    5   6   7   8   9  10  11
#   12  13  14  15  16  17  18
#   19  20  21  22  23  24  25
#   26  27  28  29

config = CalendarConfig(cell_width=6, left_pad=0)
print(render_month(2024, 2, config=config))
```

## Why

Generating a plain-text calendar grid is a small but fiddly task: weekday alignment, leading/trailing blank days, and leap-year February all need to be handled consistently. This library delegates date arithmetic to the standard library `calendar` module and focuses only on the formatting decision — outside-month days are spaces, not adjacent dates, so the reader never mistakes a 31 from January for a February day.

## Edge cases

- February in leap years produces a sixth week row (e.g., 2024); non-leap Februaries may produce five rows.
- Months whose first day is not Monday will have leading blank cells.
- Months whose last day is not Sunday will have trailing blank cells.
- `render_month` raises `ValueError` for month values outside 1–12.
