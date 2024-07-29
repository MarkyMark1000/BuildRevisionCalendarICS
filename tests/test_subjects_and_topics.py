from unittest import mock

import pytest

from ..helpers.SubjectsAndTopics import subject, subject_loader, topic


class TestSubjectLoader:

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
