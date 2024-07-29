import datetime as dt
from abc import ABC, abstractmethod

from .constants import C_LOGGING, C_SCHOOLDAY_CUTOFF_HOUR


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


class TransformStartOfDay(BaseDateTransformer):

    def transform(self, input_datetime: dt.datetime) -> dt.datetime:
        dt_temp = input_datetime
        dt_temp = dt_temp.replace(hour=9, minute=0)
        self._log(dt_temp)
        return dt_temp


class TransformAfterSchoolOr1Hour(BaseDateTransformer):

    def transform(self, input_datetime: dt.datetime) -> dt.datetime:
        ret = input_datetime + dt.timedelta(hours=1)
        if ret.hour <= C_SCHOOLDAY_CUTOFF_HOUR:
            ret = ret.replace(hour=C_SCHOOLDAY_CUTOFF_HOUR, minute=0)
        return ret
