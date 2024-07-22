import datetime as dt

import pytest

from ..helpers.InvalidDates import InvalidDates
from ..helpers.InvalidWeekdayAndHour import InvalidWeekdayAndHour
from ..helpers.SchoolHolidays import SchoolHolidays
from ..helpers.TimeAdjuster import TimeAdjuster


class TestTimeAdjuster:
    """
    Key test criterea:
        - lunch and dinner
        - invalid weekday and hours (setup data)
        - invalid dates (setup data)
        - school holidays and weekends (9am to 8pm)
        - normal school days (6pm to 8pm)
    """

    def setup_method(self):
        # setup the Time Adjuster, but don't make the other
        # classes part of the test class
        objSH = SchoolHolidays()
        objID = InvalidDates()
        objIWH = InvalidWeekdayAndHour()
        self.objTimeAdjuster = TimeAdjuster(
            invalid_dates=objID, school_holidays=objSH, invalid_weekday_and_hour=objIWH
        )

    def test_lunch(self):

        dt_test = dt.datetime(year=2024, month=7, day=13, hour=12)

        new_date = self.objTimeAdjuster.validate_or_find_next(dt_test)

        assert dt_test.year == new_date.year
        assert dt_test.month == new_date.month
        assert dt_test.day == new_date.day
        assert dt_test.hour == new_date.hour - 1

    def test_dinner(self):

        dt_test = dt.datetime(year=2024, month=7, day=13, hour=17)

        new_date = self.objTimeAdjuster.validate_or_find_next(dt_test)

        assert dt_test.year == new_date.year
        assert dt_test.month == new_date.month
        assert dt_test.day == new_date.day
        assert dt_test.hour == new_date.hour - 1

    def test_invalid_weekday_and_time(self):

        dt_test = dt.datetime(year=2024, month=7, day=10, hour=18)
        # evening of the next school day
        dt_expected = dt.datetime(year=2024, month=7, day=11, hour=18)

        new_date = self.objTimeAdjuster.validate_or_find_next(dt_test)

        assert dt_expected.year == new_date.year
        assert dt_expected.month == new_date.month
        assert dt_expected.day == new_date.day
        assert dt_expected.hour == new_date.hour

    def test_invalid_date(self):

        # Christmas Day
        dt_test = dt.datetime(year=2024, month=12, day=25, hour=18)
        # Morning after boxing day
        dt_expected = dt.datetime(year=2024, month=12, day=27, hour=9)

        new_date = self.objTimeAdjuster.validate_or_find_next(dt_test)

        assert dt_expected.year == new_date.year
        assert dt_expected.month == new_date.month
        assert dt_expected.day == new_date.day
        assert dt_expected.hour == new_date.hour

    def test_school_holiday(self):

        dt_test = dt.datetime(year=2024, month=7, day=25, hour=9)
        # School holidays should be valid, so no need for a time change
        dt_expected = dt.datetime(year=2024, month=7, day=25, hour=9)

        new_date = self.objTimeAdjuster.validate_or_find_next(dt_test)

        assert dt_expected.year == new_date.year
        assert dt_expected.month == new_date.month
        assert dt_expected.day == new_date.day
        assert dt_expected.hour == new_date.hour

    def test_school_day_ok(self):

        dt_test = dt.datetime(year=2024, month=7, day=11, hour=18)
        # school days shouldn't change
        dt_expected = dt.datetime(year=2024, month=7, day=11, hour=18)

        new_date = self.objTimeAdjuster.validate_or_find_next(dt_test)

        assert dt_expected.year == new_date.year
        assert dt_expected.month == new_date.month
        assert dt_expected.day == new_date.day
        assert dt_expected.hour == new_date.hour

    def test_school_day_too_early(self):

        dt_test = dt.datetime(year=2024, month=7, day=11, hour=9)
        # school days change if they are too early
        dt_expected = dt.datetime(year=2024, month=7, day=11, hour=18)

        new_date = self.objTimeAdjuster.validate_or_find_next(dt_test)

        assert dt_expected.year == new_date.year
        assert dt_expected.month == new_date.month
        assert dt_expected.day == new_date.day
        assert dt_expected.hour == new_date.hour
