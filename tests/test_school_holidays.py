import datetime as dt

from ..helpers.SchoolHolidays import SchoolHolidays


class TestSchoolHolidays:

    def test_school_holiday_false(self):

        # initiate the class
        objSH = SchoolHolidays()

        # This date should not be in the school holiday
        dt_test = dt.datetime(year=2024, month=9, day=20)

        result = objSH.is_within_school_holiday(dt_test)

        assert not result

    def test_school_holiday_true(self):

        # initiate the class
        objSH = SchoolHolidays()

        # This date should not be in the school holiday
        dt_test = dt.datetime(year=2024, month=8, day=1)

        result = objSH.is_within_school_holiday(dt_test)

        assert result

    def test_school_holiday_last_day_true(self):

        # initiate the class
        objSH = SchoolHolidays()

        # This date should not be in the school holiday
        dt_test = dt.datetime(year=2024, month=9, day=3, hour=20)

        result = objSH.is_within_school_holiday(dt_test)

        assert result
