import datetime as dt
from unittest import mock

import pytest

from ..helpers.constants import C_DATESTEPS
from ..helpers.SubjectsAndTopics import subject, subject_loader, topic


class TestSubjectLoader:

    def test_timedelta_upper_and_lower(self):

        objSL = subject_loader()

        for k in C_DATESTEPS.keys():

            td = objSL._get_timedelta(k)
            assert isinstance(td, dt.timedelta)

            k_u = k.upper()
            td = objSL._get_timedelta(k_u)
            assert isinstance(td, dt.timedelta)

            k_l = k.lower()
            td = objSL._get_timedelta(k_l)
            assert isinstance(td, dt.timedelta)

    def test_timedelta_not_present(self):

        objSL = subject_loader()

        with pytest.raises(Exception):

            objSL._get_timedelta("bob the builder")

    @mock.patch.object(subject_loader, "_load_topics")
    def test_return_subject(self, mock_load_topics):

        mock_load_topics.return_value = [
            topic(description="Test Topic", timedelta_key="None", timedelta=None)
        ]

        objSL = subject_loader()

        ret = objSL.load(name="Test Subject", path="/bin/")

        assert isinstance(ret, subject)
        assert ret.name == "Test Subject"
