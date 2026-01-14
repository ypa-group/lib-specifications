from datetime import date, datetime, timedelta

from ...core import BaseCallback


class IsWeekendCallback(BaseCallback):
    """Check if a date falls on a weekend.
    Example:
        >>> IsWeekendCallback(date(2026, 1, 1)).__call__()
        False
        >>> IsWeekendCallback(date(2026, 1, 4)).__call__()
        True
    """

    qualname = "isWeekend"

    def __init__(self, dt: date):
        self.dt = dt

    def __call__(self) -> bool:
        return self.dt.weekday() >= 5


class IsTodayCallback(BaseCallback):
    """Check if a date is today
    Example:
        >>> IsTodayCallback(date(2026, 1, 1)).__call__()
        False
        >>> IsTodayCallback(date.today()).__call__()
        True
    """

    qualname = "isToday"

    def __init__(self, dt: date):
        self.dt = dt

    def __call__(self) -> bool:
        return self.dt == date.today()


class IsDayAfterTodayCallback(BaseCallback):
    """Check if a date is a specified number of days after today.

    Args:
        dt: The date to check
        days: Number of days after today to check for
        strict: If True, the date must be exactly N days after today.
                If False, the date must be at least N days after today.

    Example:
        >>> IsDayAfterTodayCallback(date(2026, 1, 1), 1).__call__()
        False
        >>> IsDayAfterTodayCallback(date.today() + timedelta(days=2), 2).__call__()
        True
        >>> IsDayAfterTodayCallback(date.today() + timedelta(days=1), 2, strict=False).__call__()
        True
    """

    qualname = "isDayAfterToday"

    def __init__(self, dt: date, days: int, strict: bool = True):
        self.dt = dt
        self.days = days
        self.strict = strict

    def __call__(self) -> bool:
        target_date = date.today() + timedelta(days=self.days)
        return self.dt == target_date if self.strict else self.dt >= target_date


class IsDayBeforeTodayCallback(BaseCallback):
    """Check if a date is a specified number of days before today.

    Args:
        dt: The date to check
        days: Number of days before today to check for
        strict: If True, the date must be exactly N days before today.
                If False, the date must be at most N days before today.

    Example:
        >>> IsDayBeforeTodayCallback(date(2026, 1, 1), 1).__call__()
        False
        >>> IsDayBeforeTodayCallback(date.today() - timedelta(days=2), 2).__call__()
        True
        >>> IsDayBeforeTodayCallback(date.today() - timedelta(days=1), 2, strict=False).__call__()
        True
    """

    qualname = "isDayBeforeToday"

    def __init__(self, dt: date, days: int, strict: bool = True):
        self.dt = dt
        self.days = days
        self.strict = strict

    def __call__(self) -> bool:
        target_date = date.today() - timedelta(days=self.days)
        return self.dt == target_date if self.strict else self.dt <= target_date


class IsDateInRangeCallback(BaseCallback):
    """Check if a date is within a specified range (inclusive).

    Args:
        dt: The date to check
        start_date: Start of the range (inclusive)
        end_date: End of the range (inclusive)

    Example:
        >>> IsDateInRangeCallback(date(2026, 1, 15), date(2026, 1, 1), date(2026, 1, 31)).__call__()
        True
        >>> IsDateInRangeCallback(date(2026, 2, 1), date(2026, 1, 1), date(2026, 1, 31)).__call__()
        False
    """

    qualname = "isDateInRange"

    def __init__(self, dt: date, start_date: date, end_date: date):
        self.dt = dt
        self.start_date = start_date
        self.end_date = end_date

    def __call__(self) -> bool:
        return self.start_date <= self.dt <= self.end_date


class IsDayNotLaterThanCallback(BaseCallback):
    """Check if a date is not later than a specified number of days from today.

    Args:
        dt: The date to check
        days: Number of days from today (can be negative for past dates)

    Example:
        >>> IsDayNotLaterThanCallback(date.today() + timedelta(days=5), 7).__call__()
        True
        >>> IsDayNotLaterThanCallback(date.today() + timedelta(days=10), 7).__call__()
        False
    """

    qualname = "isDayNotLaterThan"

    def __init__(self, dt: date, days: int):
        self.dt = dt
        self.days = days

    def __call__(self) -> bool:
        return self.dt <= date.today() + timedelta(days=self.days)


class IsPastDateCallback(BaseCallback):
    """Check if a date is in the past (before today).

    Args:
        dt: The date to check

    Example:
        >>> IsPastDateCallback(date.today() - timedelta(days=1)).__call__()
        True
        >>> IsPastDateCallback(date.today()).__call__()
        False
        >>> IsPastDateCallback(date.today() + timedelta(days=1)).__call__()
        False
    """

    qualname = "isPastDate"

    def __init__(self, dt: date):
        self.dt = dt

    def __call__(self) -> bool:
        return self.dt < date.today()


class IsFutureDateCallback(BaseCallback):
    """Check if a date is in the future (after today).

    Args:
        dt: The date to check

    Example:
        >>> IsFutureDateCallback(date.today() + timedelta(days=1)).__call__()
        True
        >>> IsFutureDateCallback(date.today()).__call__()
        False
        >>> IsFutureDateCallback(date.today() - timedelta(days=1)).__call__()
        False
    """

    qualname = "isFutureDate"

    def __init__(self, dt: date):
        self.dt = dt

    def __call__(self) -> bool:
        return self.dt > date.today()


class IsWithinDaysCallback(BaseCallback):
    """Check if a date is within a specified number of days from today (before or after).

    Args:
        dt: The date to check
        days: Number of days from today (absolute value)

    Example:
        >>> IsWithinDaysCallback(date.today() + timedelta(days=3), 5).__call__()
        True
        >>> IsWithinDaysCallback(date.today() - timedelta(days=3), 5).__call__()
        True
        >>> IsWithinDaysCallback(date.today() + timedelta(days=10), 5).__call__()
        False
    """

    qualname = "isWithinDays"

    def __init__(self, dt: date, days: int):
        self.dt = dt
        self.days = days

    def __call__(self) -> bool:
        today = date.today()
        diff = abs((self.dt - today).days)
        return diff <= self.days


class IsSameDayOfWeekCallback(BaseCallback):
    """Check if a date falls on the same day of week as another date.

    Args:
        dt: The date to check
        reference_date: The reference date to compare against

    Example:
        >>> IsSameDayOfWeekCallback(date(2026, 1, 5), date(2026, 1, 12)).__call__()
        True  # Both are Mondays
        >>> IsSameDayOfWeekCallback(date(2026, 1, 5), date(2026, 1, 6)).__call__()
        False
    """

    qualname = "isSameDayOfWeek"

    def __init__(self, dt: date, reference_date: date):
        self.dt = dt
        self.reference_date = reference_date

    def __call__(self) -> bool:
        return self.dt.weekday() == self.reference_date.weekday()


class IsDayOfMonthCallback(BaseCallback):
    """Check if a date falls on a specific day of the month.

    Args:
        dt: The date to check
        day_of_month: Day of the month (1-31)

    Example:
        >>> IsDayOfMonthCallback(date(2026, 1, 15), 15).__call__()
        True
        >>> IsDayOfMonthCallback(date(2026, 1, 20), 15).__call__()
        False
    """

    qualname = "isDayOfMonth"

    def __init__(self, dt: date, day_of_month: int):
        self.dt = dt
        self.day_of_month = day_of_month

    def __call__(self) -> bool:
        return self.dt.day == self.day_of_month


class IsSameMonthCallback(BaseCallback):
    """Check if a date is in the same month and year as another date.

    Args:
        dt: The date to check
        reference_date: The reference date to compare against

    Example:
        >>> IsSameMonthCallback(date(2026, 1, 15), date(2026, 1, 31)).__call__()
        True
        >>> IsSameMonthCallback(date(2026, 1, 15), date(2026, 2, 1)).__call__()
        False
    """

    qualname = "isSameMonth"

    def __init__(self, dt: date, reference_date: date):
        self.dt = dt
        self.reference_date = reference_date

    def __call__(self) -> bool:
        return self.dt.year == self.reference_date.year and self.dt.month == self.reference_date.month


class IsSameYearCallback(BaseCallback):
    """Check if a date is in the same year as another date.

    Args:
        dt: The date to check
        reference_date: The reference date to compare against

    Example:
        >>> IsSameYearCallback(date(2026, 1, 15), date(2026, 12, 31)).__call__()
        True
        >>> IsSameYearCallback(date(2026, 1, 15), date(2027, 1, 1)).__call__()
        False
    """

    qualname = "isSameYear"

    def __init__(self, dt: date, reference_date: date):
        self.dt = dt
        self.reference_date = reference_date

    def __call__(self) -> bool:
        return self.dt.year == self.reference_date.year


class IsDayNotEarlierThanCallback(BaseCallback):
    """Check if a date is not earlier than a specified number of days from today.

    Args:
        dt: The date to check
        days: Number of days from today (can be negative for future dates)

    Example:
        >>> IsDayNotEarlierThanCallback(date.today() - timedelta(days=5), 7).__call__()
        True
        >>> IsDayNotEarlierThanCallback(date.today() - timedelta(days=10), 7).__call__()
        False
    """

    qualname = "isDayNotEarlierThan"

    def __init__(self, dt: date, days: int):
        self.dt = dt
        self.days = days

    def __call__(self) -> bool:
        return self.dt >= date.today() + timedelta(days=self.days)


class IsTimeAfterCallback(BaseCallback):
    """Check if a datetime is not earlier than specified gap before now.

    Returns True if the check_datetime is within the last 'gap_hours' hours,
    meaning it's not earlier than (now - gap_hours).

    Args:
        check_datetime: The datetime to check
        gap_hours: Number of hours to check back from now

    Example:
        >>> from datetime import datetime, timedelta
        >>> now = datetime.now()
        >>> # Datetime 2 hours ago - should return True (within 3 hours)
        >>> IsTimeAfterCallback(now - timedelta(hours=2), 3).__call__()
        True
        >>> # Datetime 4 hours ago - should return False (outside 3 hours)
        >>> IsTimeAfterCallback(now - timedelta(hours=4), 3).__call__()
        False
    """

    qualname = "isTimeAfter"

    def __init__(self, check_datetime: datetime, gap_hours: float):
        self.check_datetime = check_datetime
        self.gap_hours = gap_hours

    def __call__(self) -> bool:
        now = datetime.now()
        gap_threshold = now - timedelta(hours=self.gap_hours)
        return self.check_datetime >= gap_threshold
