import pytest
import datetime as dt

from ..helpers.InvalidWeekdayAndHour import InvalidWeekdayAndHour

class TestSchoolHolidays:

    def test_invalid_false(self):

        # initiate the class
        objID = InvalidWeekdayAndHour()

        # Pick a monday
        dt_test = dt.datetime(year=2024, month=6, day=17, hour=18)

        result = objID.is_invalid_weekday_and_hour(dt_test)

        assert not result

    def test_invalid_date_true(self):

        # initiate the class
        objID = InvalidWeekdayAndHour()

        # This date should not be in the school holiday
        dt_test = dt.datetime(year=2024, month=6, day=19, hour=18)

        result = objID.is_invalid_weekday_and_hour(dt_test)

        assert result
