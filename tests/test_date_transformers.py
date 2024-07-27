import datetime as dt

from ..helpers.constants import C_SCHOOLDAY_CUTOFF_HOUR
from ..helpers.DateCheckers import Transform1Hour, TransformAfterSchoolOr1Hour, TransformNextDay


class TestDateTransformers:

    def test_transform_1_hour(self):

        objID = Transform1Hour()
        test_dt = dt.datetime(year=2024, month=1, day=1, hour=12, minute=3)
        test_new_dt = objID.transform(test_dt)

        assert (test_new_dt - test_dt).total_seconds() == (60 * 60)

    def test_transform_next_day(self):

        objID = TransformNextDay()
        test_dt = dt.datetime(year=2024, month=1, day=1, hour=12, minute=3)
        test_new_dt = objID.transform(test_dt)

        assert test_new_dt.day == 2
        assert test_new_dt.hour == 9

    def test_after_school(self):

        objID = TransformAfterSchoolOr1Hour()
        test_dt = dt.datetime(year=2024, month=1, day=1, hour=12)
        test_new_dt = objID.transform(test_dt)

        assert test_new_dt.day == 1
        assert test_new_dt.hour == C_SCHOOLDAY_CUTOFF_HOUR

    def test_after_school_by_1_hour(self):

        objID = TransformAfterSchoolOr1Hour()
        test_dt = dt.datetime(year=2024, month=1, day=1, hour=C_SCHOOLDAY_CUTOFF_HOUR)
        test_new_dt = objID.transform(test_dt)

        assert test_new_dt.day == 1
        assert test_new_dt.hour == C_SCHOOLDAY_CUTOFF_HOUR + 1
