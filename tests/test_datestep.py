
import datetime as dt
from unittest import mock

import pytest

from ..helpers.DateSteps import C_DATESTEPS, datestep

# test fetching the next datestep

class TestDateStep:

    def test_no_step(self):

        objDS = datestep(
            input_datetime=dt.datetime.now(),
        )

        assert objDS._datestep.upper() == "NOW"


    def test_invalid_key(self):

        key = "1 mownth"

        with pytest.raises(Exception):

            objDS = datestep(
                input_datetime=dt.datetime.now(),
                current_step = key
            )

    def test_adjust_datetime(self):

        delta = dt.timedelta(days=1)
        now_dt = dt.datetime.now()

        objDS = datestep(
            input_datetime=now_dt
        )

        objDS.current_datetime = (objDS.current_datetime + delta)

        assert objDS.current_datetime == (now_dt + delta)

    def test_next_datestep(self):

        now_dt = dt.datetime.now()
        delta = dt.timedelta(hours=1)

        objDS = datestep(
            input_datetime=now_dt,
            current_step = "now"
        )

        objNewDS = objDS.get_next_datestep()

        assert isinstance(objNewDS, datestep)
        assert objNewDS._datestep.upper() == "1 HOUR"
        assert objNewDS.current_datetime == (now_dt + delta)

    def test_fetch_last_datestep(self):

        now_dt = dt.datetime.now()

        keys = tuple(C_DATESTEPS.keys())

        objDS = datestep(
            input_datetime=now_dt,
            current_step = keys[-1]
        )

        objNewDS = objDS.get_next_datestep()

        assert objNewDS is None
