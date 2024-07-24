import datetime as dt
from unittest import mock

from ..helpers.constants import C_SCHOOLDAY_CUTOFF_HOUR
from ..helpers.DateCheckers import (
                                    CheckIsDinnerTime,
                                    CheckIsLunchTime)
from ..helpers.DateCheckers import Transform1Hour
from ..helpers.DCTContainer import DCTContainer

class TestDCTContainer:

    def test_basic_dct_container(self):
        """
        We are going to test a basic example of the DCTContainer and assume
        the date_checkers and date_transformers tests covers most of the
        details
        """
        objContainer = DCTContainer(
            date_checkers=[
                CheckIsLunchTime(),
                CheckIsDinnerTime()
            ],
            date_transformers=[
                Transform1Hour(),
                Transform1Hour()
            ]
        )

        dt_lunch = dt.datetime(year=2024,
                               month=7,
                               day=24,
                               hour=12)
        dt_result = objContainer.transform(input_datetime=dt_lunch)

        assert dt_result.hour == 13
        assert (dt_result-dt_lunch).total_seconds() < (60*60+1)

        dt_dinner = dt.datetime(year=2024,
                               month=7,
                               day=24,
                               hour=17)
        dt_result = objContainer.transform(input_datetime=dt_dinner)

        assert dt_result.hour == 18
        assert (dt_result-dt_dinner).total_seconds() < (60*60+1)