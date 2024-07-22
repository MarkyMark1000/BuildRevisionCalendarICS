import datetime as dt
from unittest import mock

from ..helpers.constants import C_SCHOOLDAY_CUTOFF_HOUR
from ..helpers.DateCheckers import (CheckInvalidDates,
                                    CheckInvalidWeekdayAndHour,
                                    CheckIsDinnerTime, CheckIsLunchTime,
                                    CheckIsPastEndOfDay,
                                    CheckSchoolHolidayTime, CheckSchoolTime,
                                    SchoolHolidayData)


class TestDateCheckers:

    def test_is_lunchtime_true(self):

        objID = CheckIsLunchTime()
        test_dt = dt.datetime(year=2024, month=1, day=1, hour=12, minute=3)
        assert objID.validate(input_datetime=test_dt)

    def test_is_lunchtime_false(self):

        objID = CheckIsLunchTime()
        test_dt = dt.datetime(year=2024, month=1, day=1, hour=13, minute=3)
        assert not objID.validate(input_datetime=test_dt)

    def test_is_dinnertime_true(self):

        objID = CheckIsDinnerTime()
        test_dt = dt.datetime(year=2024, month=1, day=1, hour=17, minute=3)
        assert objID.validate(input_datetime=test_dt)

    def test_is_dinnertime_false(self):

        objID = CheckIsDinnerTime()
        test_dt = dt.datetime(year=2024, month=1, day=1, hour=18, minute=3)
        assert not objID.validate(input_datetime=test_dt)

    def test_is_endofday_true(self):

        objID = CheckIsPastEndOfDay()
        test_dt = dt.datetime(year=2024, month=1, day=1, hour=21, minute=3)
        assert objID.validate(input_datetime=test_dt)

    def test_is_endofday_false(self):

        objID = CheckIsPastEndOfDay()
        test_dt = dt.datetime(year=2024, month=1, day=1, hour=19, minute=3)
        assert not objID.validate(input_datetime=test_dt)

    @mock.patch.object(CheckInvalidDates, "_load_dates")
    def test_invalid_dates_true(self, mock_load_dates):

        mock_load_dates.return_value = [dt.datetime(year=2024, month=12, day=25)]

        objID = CheckInvalidDates(path=None)

        dt_christmas = dt.datetime(year=2024, month=12, day=25)

        assert objID.validate(dt_christmas)

    @mock.patch.object(CheckInvalidDates, "_load_dates")
    def test_invalid_dates_false(self, mock_load_dates):

        mock_load_dates.return_value = [dt.datetime(year=2024, month=12, day=25)]

        objID = CheckInvalidDates(path=None)

        dt_12 = dt.datetime(year=2024, month=12, day=12)

        assert not objID.validate(dt_12)

    def test_weekday_and_hour_converter(self):

        objID = CheckInvalidWeekdayAndHour(path=None)

        assert objID._get_weekday_from_string("monday") == 0
        assert objID._get_weekday_from_string("SunDay") == 6

    @mock.patch.object(CheckInvalidWeekdayAndHour, "_load_file")
    def test_invalid_weekday_time_true(self, mock_load_file):

        mock_load_file.return_value = [{"weekday": 0, "hour": 16}]

        objID = CheckInvalidWeekdayAndHour(path=None)

        dt_test = dt.datetime(year=2024, month=7, day=22, hour=16, minute=5)

        assert objID.validate(input_datetime=dt_test)

    @mock.patch.object(CheckInvalidWeekdayAndHour, "_load_file")
    def test_invalid_weekday_time_false(self, mock_load_file):

        mock_load_file.return_value = [{"weekday": 0, "hour": 16}]

        objID = CheckInvalidWeekdayAndHour(path=None)

        dt_test = dt.datetime(year=2024, month=7, day=22, hour=15, minute=5)

        assert not objID.validate(input_datetime=dt_test)

    @mock.patch.object(SchoolHolidayData, "_load_school_holidays")
    def test_is_in_school_holiday(self, mock_load_school_holidays):

        mock_load_school_holidays.return_value = [
            {
                "start_date": dt.datetime(year=2024, month=7, day=24),
                "end_date": dt.datetime(year=2024, month=9, day=3, hour=23),
            }
        ]

        objID = SchoolHolidayData(path=None)

        dt_test = dt.datetime(year=2024, month=8, day=1)

        assert objID.validate(input_datetime=dt_test)

    @mock.patch.object(SchoolHolidayData, "_load_school_holidays")
    def test_is_before_school_holiday(self, mock_load_school_holidays):

        mock_load_school_holidays.return_value = [
            {
                "start_date": dt.datetime(year=2024, month=7, day=24),
                "end_date": dt.datetime(year=2024, month=9, day=3, hour=23),
            }
        ]

        objID = SchoolHolidayData(path=None)

        dt_test = dt.datetime(year=2024, month=6, day=1)

        assert not objID.validate(input_datetime=dt_test)

    @mock.patch.object(SchoolHolidayData, "_load_school_holidays")
    def test_is_after_school_holiday(self, mock_load_school_holidays):

        mock_load_school_holidays.return_value = [
            {
                "start_date": dt.datetime(year=2024, month=7, day=24),
                "end_date": dt.datetime(year=2024, month=9, day=3, hour=23),
            }
        ]

        objID = SchoolHolidayData(path=None)

        dt_test = dt.datetime(year=2024, month=10, day=1)

        assert not objID.validate(input_datetime=dt_test)

    @mock.patch.object(CheckInvalidWeekdayAndHour, "_load_file")
    @mock.patch.object(SchoolHolidayData, "_load_school_holidays")
    def test_school_time_too_early(self, mock_load_school_holidays, mock_load_file):

        mock_load_file.return_value = [{"weekday": 0, "hour": 19}]

        mock_load_school_holidays.return_value = [
            {
                "start_date": dt.datetime(year=2024, month=7, day=24),
                "end_date": dt.datetime(year=2024, month=9, day=3, hour=23),
            }
        ]

        objWDH = CheckInvalidWeekdayAndHour(path=None)
        objID = CheckSchoolTime(invalid_weekday_and_hour=objWDH, path=None)

        dt_test = dt.datetime(year=2024, month=7, day=22, hour=11, minute=5)

        assert objID.validate(input_datetime=dt_test)

    @mock.patch.object(CheckInvalidWeekdayAndHour, "_load_file")
    @mock.patch.object(SchoolHolidayData, "_load_school_holidays")
    def test_school_time_match_invalid(self, mock_load_school_holidays, mock_load_file):

        mock_load_file.return_value = [{"weekday": 0, "hour": 19}]

        mock_load_school_holidays.return_value = [
            {
                "start_date": dt.datetime(year=2024, month=7, day=24),
                "end_date": dt.datetime(year=2024, month=9, day=3, hour=23),
            }
        ]

        objWDH = CheckInvalidWeekdayAndHour(path=None)
        objID = CheckSchoolTime(invalid_weekday_and_hour=objWDH, path=None)

        dt_test = dt.datetime(year=2024, month=7, day=22, hour=19, minute=5)

        assert objID.validate(input_datetime=dt_test)

    @mock.patch.object(CheckInvalidWeekdayAndHour, "_load_file")
    @mock.patch.object(SchoolHolidayData, "_load_school_holidays")
    def test_school_time_ok(self, mock_load_school_holidays, mock_load_file):

        mock_load_file.return_value = [{"weekday": 0, "hour": 19}]

        mock_load_school_holidays.return_value = [
            {
                "start_date": dt.datetime(year=2024, month=7, day=24),
                "end_date": dt.datetime(year=2024, month=9, day=3, hour=23),
            }
        ]

        objWDH = CheckInvalidWeekdayAndHour(path=None)
        objID = CheckSchoolTime(invalid_weekday_and_hour=objWDH, path=None)

        dt_test = dt.datetime(year=2024, month=7, day=22, hour=18, minute=5)

        assert not objID.validate(input_datetime=dt_test)

    @mock.patch.object(CheckInvalidWeekdayAndHour, "_load_file")
    @mock.patch.object(SchoolHolidayData, "_load_school_holidays")
    def test_school_holiday_time_early_but_ok(
        self, mock_load_school_holidays, mock_load_file
    ):

        mock_load_file.return_value = [{"weekday": 0, "hour": 19}]

        mock_load_school_holidays.return_value = [
            {
                "start_date": dt.datetime(year=2024, month=7, day=24),
                "end_date": dt.datetime(year=2024, month=9, day=3, hour=23),
            }
        ]

        objWDH = CheckInvalidWeekdayAndHour(path=None)
        objID = CheckSchoolHolidayTime(invalid_weekday_and_hour=objWDH, path=None)

        dt_test = dt.datetime(year=2024, month=7, day=29, hour=11, minute=5)

        assert not objID.validate(input_datetime=dt_test)

    @mock.patch.object(CheckInvalidWeekdayAndHour, "_load_file")
    @mock.patch.object(SchoolHolidayData, "_load_school_holidays")
    def test_school_holiday_time_match_invalid(
        self, mock_load_school_holidays, mock_load_file
    ):

        mock_load_file.return_value = [{"weekday": 0, "hour": 19}]

        mock_load_school_holidays.return_value = [
            {
                "start_date": dt.datetime(year=2024, month=7, day=24),
                "end_date": dt.datetime(year=2024, month=9, day=3, hour=23),
            }
        ]

        objWDH = CheckInvalidWeekdayAndHour(path=None)
        objID = CheckSchoolHolidayTime(invalid_weekday_and_hour=objWDH, path=None)

        dt_test = dt.datetime(year=2024, month=7, day=29, hour=19, minute=5)

        assert objID.validate(input_datetime=dt_test)

    @mock.patch.object(CheckInvalidWeekdayAndHour, "_load_file")
    @mock.patch.object(SchoolHolidayData, "_load_school_holidays")
    def test_school_holiday_time_ok(self, mock_load_school_holidays, mock_load_file):

        mock_load_file.return_value = [{"weekday": 0, "hour": 19}]

        mock_load_school_holidays.return_value = [
            {
                "start_date": dt.datetime(year=2024, month=7, day=24),
                "end_date": dt.datetime(year=2024, month=9, day=3, hour=23),
            }
        ]

        objWDH = CheckInvalidWeekdayAndHour(path=None)
        objID = CheckSchoolHolidayTime(invalid_weekday_and_hour=objWDH, path=None)

        dt_test = dt.datetime(year=2024, month=7, day=29, hour=18, minute=5)

        assert not objID.validate(input_datetime=dt_test)
