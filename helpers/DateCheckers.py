import datetime as dt
from abc import ABC, abstractmethod
from typing import Any

from .constants import C_LOGGING, C_SCHOOLDAY_CUTOFF_HOUR


class BaseDateChecker(ABC):
    """Abstract Base datechecker class."""

    def _log(self, value: Any) -> None:
        if C_LOGGING:
            print(self.__class__.__name__, ": ", value)

    @abstractmethod
    def validate(self, input_datetime: dt.datetime) -> bool:
        """Validate input_datetime."""
        pass


class CheckIsLunchTime(BaseDateChecker):
    """Check if lunchtime."""

    def validate(self, input_datetime: dt.datetime) -> bool:
        """Check if lunchtime."""
        ret = input_datetime.hour == 12
        self._log(ret)
        return ret


class CheckIsDinnerTime(BaseDateChecker):
    """Check if dinnertime."""

    def validate(self, input_datetime: dt.datetime) -> bool:
        """Check if dinnertime."""
        ret = input_datetime.hour == 17
        self._log(ret)
        return ret


class CheckIsPastEndOfDay(BaseDateChecker):
    """Check if past end of day, ie 20:00."""

    def validate(self, input_datetime: dt.datetime) -> bool:
        """Check if past end of day, ie 20:00."""
        ret = input_datetime.hour > 20
        self._log(ret)
        return ret


class CheckIsBeforeStartOfDay(BaseDateChecker):
    """Check if before start of day, ie 9:00."""

    def validate(self, input_datetime: dt.datetime) -> bool:
        """Check if before start of day, ie 9:00."""
        ret = input_datetime.hour < 9
        self._log(ret)
        return ret


class CheckInvalidDates(BaseDateChecker):
    """Compare datetime to a file of invalid datetimes."""

    _data: list[dt.datetime]

    def _load_dates(self, path: str) -> list[dt.datetime]:

        ret: list[dt.datetime] = list()
        if not path:
            return ret

        with open(path, "r") as file:
            for line in file:

                date_value = line.strip()
                date_dt = dt.datetime.strptime(date_value, "%d-%B-%Y")
                ret.append(date_dt)

        return ret

    def __init__(self, path: str="setup_data/Control Files/invalid_dates.txt"):

        self._data = self._load_dates(path)

    def validate(self, input_datetime: dt.datetime) -> bool:
        """Compare datetime to a file of invalid datetimes."""
        ret = False
        for row in self._data:
            if input_datetime.date() == row.date():
                ret = True
                break

        self._log(ret)
        return ret


"""
This is slightly more complicated.   We have invalid weekday and
hours for school holidays and for school days.   We need to first
check if the datetime is a school holiday, but then check the
datetime against those files.
"""


class CheckInvalidWeekdayAndHour(BaseDateChecker):
    """Compare datetime to a file of invalid weekday and hours."""

    _data: list[dict[str,int]]

    def __init__(self, path: str="setup_data/Control Files/invalid_weekday_and_time.txt"):

        self._data = self._load_file(path)

    def _get_weekday_from_string(self, string_weekday: str) -> int:
        """Returns number value for weekday, ie Monday=0."""
        weekday = string_weekday.upper().strip()

        wd = 0
        if weekday == "SUNDAY":
            wd = 6
        elif weekday == "MONDAY":
            wd = 0
        elif weekday == "TUESDAY":
            wd = 1
        elif weekday == "WEDNESDAY":
            wd = 2
        elif weekday == "THURSDAY":
            wd = 3
        elif weekday == "FRIDAY":
            wd = 4
        elif weekday == "SATURDAY":
            wd = 5
        else:
            raise Exception(f"Invalid weekday: {weekday}")

        return wd

    def _load_file(self, path: str) -> list[dict[str,int]]:
        """Loads the datafile into a list [{'weekday': 0, 'hour': 12}, ....]."""
        ret: list[dict[str,int]] = list()
        if not path:
            return ret

        with open(path, "r") as file:
            for line in file:

                line_strip = line.strip()
                if len(line_strip) > 0:
                    line_values = line_strip.split(" ")

                    weekday = line_values[0]

                    hour = line_values[1]
                    hour_ar = hour.split(":")
                    hour_int = int(hour_ar[0])

                    wd = self._get_weekday_from_string(weekday)

                    ret.append({"weekday": wd, "hour": hour_int})

        return ret

    def validate(self, input_datetime: dt.datetime) -> bool:
        """Compare datetime to a file of invalid weekday and hours."""
        ret = False
        for row in self._data:
            if input_datetime.weekday() == row["weekday"] and input_datetime.hour == row["hour"]:
                ret = True
                break

        self._log(ret)

        return ret


class SchoolHolidayData(BaseDateChecker):
    """Compare datetime to a file of school hoidays."""

    _data: list[dict[str,dt.datetime]]

    def _load_school_holidays(self, path: str) -> list[dict[str,dt.datetime]]:

        ret: list[dict[str,dt.datetime]] = list()
        if not path:
            return ret

        with open(path, "r") as file:
            for line in file:
                rdata = line.split(",")
                start_date = rdata[0].strip()
                end_date = rdata[1].strip()
                start_date_dt = dt.datetime.strptime(start_date, "%d-%B-%Y")
                end_date_dt = dt.datetime.strptime(end_date, "%d-%B-%Y").replace(hour=23, minute=59)
                if (end_date_dt - start_date_dt).total_seconds() < 0:
                    raise Exception(f"Invalid Start/End date: {start_date_dt}, {end_date_dt}")
                ret.append({"start_date": start_date_dt, "end_date": end_date_dt})

        return ret

    def __init__(self, path: str="setup_data/Control Files/school_holidays.txt"):

        self._data = self._load_school_holidays(path=path)

    def validate(self, input_datetime: dt.datetime) -> bool:
        """Compare datetime to a file of school hoidays."""
        ret = False
        for row in self._data:
            if (input_datetime - row["start_date"]).total_seconds() >= 0 and (
                input_datetime - row["end_date"]
            ).total_seconds() <= 0:

                ret = True
                break

        self._log(ret)
        return ret


class CheckSchoolTime(SchoolHolidayData):
    """Combine check of valid weekday and time when not in school holidays."""

    def __init__(
        self,
        invalid_weekday_and_hour: CheckInvalidWeekdayAndHour,
        path: str = "setup_data/Control Files/school_holidays.txt",
    ):

        # Call the super class to initate with dates and times
        super().__init__(path=path)

        # Add invalid weekday and hour for School Times
        self._invalid_weekday_and_hour = invalid_weekday_and_hour

    def validate(self, input_datetime: dt.datetime) -> bool:
        """Combine check of valid weekday and time when not in school holidays."""
        # Is it a school holiday:
        ret = super().validate(input_datetime=input_datetime)

        # If not a school holiday, less than 18:00 or within the invalid
        # date and time, then check here
        ret = (not ret) and (
            input_datetime.hour < C_SCHOOLDAY_CUTOFF_HOUR
            or self._invalid_weekday_and_hour.validate(input_datetime=input_datetime)
        )

        self._log(ret)
        return ret


class CheckSchoolHolidayTime(SchoolHolidayData):
    """Combine check of valid weekday and time with school holiday."""

    def __init__(
        self,
        invalid_weekday_and_hour: CheckInvalidWeekdayAndHour,
        path: str = "setup_data/Control Files/school_holidays.txt",
    ):

        # Call the super class to initate with dates and times
        super().__init__(path=path)

        # Add invalid weekday and hour for School Holiday Times
        self._invalid_weekday_and_hour = invalid_weekday_and_hour

    def validate(self, input_datetime: dt.datetime) -> bool:
        """Combine check of valid weekday and time with school holiday."""
        # Is it a school holiday:
        ret = super().validate(input_datetime=input_datetime)

        # If a school holiday and invalid weekday/hour
        ret = ret and self._invalid_weekday_and_hour.validate(input_datetime=input_datetime)

        self._log(ret)
        return ret
