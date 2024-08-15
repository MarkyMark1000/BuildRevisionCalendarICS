from unittest import mock

import pytest

from ..helpers.SubjectsAndTopics import subject, subject_loader, subjects_loader, topic


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

    def test_load_file(self):

        objSL = subject_loader()

        ret = objSL.load(name="Test Subject", path="tests/test_data/1Hr Files/test_subject.txt")

        assert isinstance(ret, subject)
        assert ret.name == "Test Subject"
        assert len(ret.topics) == 2
        assert ret.topics[0].description == "1.1 to 1.2"
        assert ret.topics[0].timedelta_key == "now"
        assert ret.topics[1].description == "1.3 to 1.4"
        assert ret.topics[1].timedelta_key == "1 hour"


class TestSubjectsLoader:

    def test_load_files(self):

        objSL = subject_loader()
        objSSL = subjects_loader(loader=objSL)

        ret = objSSL.load(directory_path="tests/test_data/1Hr Files")

        assert isinstance(ret, list)
        assert len(ret) == 1
        assert isinstance(ret[0], subject)
