import pytest
import datetime as dt

from ..helpers.InvalidDates import InvalidDates

class TestSchoolHolidays:

    def test_invalid_date_false(self):

        # initiate the class
        objID = InvalidDates()

        # This date should not be in the school holiday
        dt_test = dt.datetime(year=2024, month=9, day=20)

        result = objID.is_invalid_date(dt_test)

        assert not result

    def test_invalid_date_true(self):

        # initiate the class
        objID = InvalidDates()

        # This date should not be in the school holiday
        dt_test = dt.datetime(year=2024, month=12, day=25)

        result = objID.is_invalid_date(dt_test)

        assert result
