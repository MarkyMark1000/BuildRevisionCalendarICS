import datetime as dt
from abc import ABC, abstractmethod

from .constants import C_LOGGING, C_SCHOOLDAY_CUTOFF_HOUR


class BaseDateChecker(ABC):

    def _log(self, value):
        if C_LOGGING:
            print(self.__class__.__name__, ": ", value)

    @abstractmethod
    def validate(self, input_datetime: dt.datetime) -> bool:
        pass


class BaseDateTransformer(ABC):

    def _log(self, value):
        if C_LOGGING:
            print(self.__class__.__name__, ": ", value)

    @abstractmethod
    def transform(self, input_datetime: dt.datetime) -> dt.datetime:
        pass


class Transform1Hour(BaseDateTransformer):

    def transform(self, input_datetime: dt.datetime) -> dt.datetime:
        ret = input_datetime + dt.timedelta(hours=1)
        self._log(ret)
        return ret


class TransformNextDay(BaseDateTransformer):

    def transform(self, input_datetime: dt.datetime) -> dt.datetime:
        dt_temp = input_datetime + dt.timedelta(days=1)
        dt_temp = dt_temp.replace(hour=9, minute=0)
        self._log(dt_temp)
        return dt_temp


class TransformAfterSchoolOr1Hour(BaseDateTransformer):

    def transform(self, input_datetime: dt.datetime) -> dt.datetime:
        ret = input_datetime + dt.timedelta(hours=1)
        if ret.hour <= C_SCHOOLDAY_CUTOFF_HOUR:
            ret = ret.replace(hour=C_SCHOOLDAY_CUTOFF_HOUR, minute=0)
        return ret


class CheckIsLunchTime(BaseDateChecker):

    def validate(self, input_datetime: dt.datetime) -> bool:
        ret = input_datetime.hour == 12
        self._log(ret)
        return ret


class CheckIsDinnerTime(BaseDateChecker):

    def validate(self, input_datetime: dt.datetime) -> bool:
        ret = input_datetime.hour == 17
        self._log(ret)
        return ret


class CheckIsPastEndOfDay(BaseDateChecker):

    def validate(self, input_datetime: dt.datetime) -> bool:
        ret = input_datetime.hour > 20
        self._log(ret)
        return ret


class CheckInvalidDates(BaseDateChecker):

    _data: list

    def _load_dates(self, path: str):

        ret = list()
        if not path:
            return ret

        with open(path, "r") as file:
            for line in file:

                date_value = line.strip()
                date_value = dt.datetime.strptime(date_value, "%d-%B-%Y")
                self._data.append(date_value)

        return ret

    def __init__(self, path="setup_data/Control Files/invalid_dates.txt"):

        self._data = self._load_dates(path)

    def validate(self, input_datetime: dt.datetime) -> bool:
        # is_invalid_date to validate
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

    _data: list

    def _get_weekday_from_string(self, string_weekday: str) -> int:
        """
        Returns number value for weekday, ie Monday=0
        """

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

    def _load_file(self, path: str):
        """
        Loads the datafile into a list such as:
        [{'weekday': 0, 'hour': 12}, ....]
        """

        ret = list()
        if not path:
            return ret

        with open(path, "r") as file:
            for line in file:

                line_strip = line.strip()
                line_values = line_strip.split(" ")

                weekday = line_values[0]

                hour = line_values[1]
                hour = hour.split(":")
                hour = int(hour[0])

                wd = self._get_weekday_from_string(weekday)

                self._data.append({"weekday": wd, "hour": hour})

        return ret

    def __init__(self, path="setup_data/Control Files/invalid_weekday_and_time.txt"):

        self._data = self._load_file(path)

    def validate(self, input_datetime: dt.datetime) -> bool:
        # Change is_invalid_weekday_and_hour to validate
        ret = False
        for row in self._data:
            if (
                input_datetime.weekday() == row["weekday"]
                and input_datetime.hour == row["hour"]
            ):
                ret = True
                break

        self._log(ret)

        return ret


class SchoolHolidayData(BaseDateChecker):

    _data: list

    def _load_school_holidays(self, path):

        ret = list()
        if not path:
            return ret

        with open(path, "r") as file:
            for line in file:
                rdata = line.split(",")
                start_date = rdata[0].strip()
                end_date = rdata[1].strip()
                start_date = dt.datetime.strptime(start_date, "%d-%B-%Y")
                end_date = dt.datetime.strptime(end_date, "%d-%B-%Y").replace(
                    hour=23, minute=59
                )
                if (end_date - start_date).total_seconds() < 0:
                    raise Exception(f"Invalid Start/End date: {start_date}, {end_date}")
                self._data.append({"start_date": start_date, "end_date": end_date})

        return ret

    def __init__(self, path="setup_data/Control Files/school_holidays.txt"):

        self._data = self._load_school_holidays(path=path)

    def validate(self, input_datetime: dt.datetime) -> bool:
        # replace is_within_school_holiday with validate
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

        # Is it a school holiday:
        ret = super().validate(input_datetime=input_datetime)

        # If a school holiday and invalid weekday/hour
        ret = ret and self._invalid_weekday_and_hour.validate(
            input_datetime=input_datetime
        )

        self._log(ret)
        return ret
