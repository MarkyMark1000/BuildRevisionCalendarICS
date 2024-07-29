import datetime as dt

from ..helpers.DateCheckers import (
    CheckIsBeforeStartOfDay,
    CheckIsDinnerTime,
    CheckIsLunchTime,
    CheckIsPastEndOfDay,
)
from ..helpers.DateSteps import C_DATESTEPS
from ..helpers.DateTransformers import Transform1Hour, TransformNextDay, TransformStartOfDay
from ..helpers.DCTContainer import DCTContainer
from ..helpers.SubjectsAndTopics import subject, topic
from ..helpers.TimeLine import TimeLineBuilder


class TestTimeLineBuilder:
    """
    This is a basic test for the timeline builder.
    """

    def _build_dct_container(self):

        return DCTContainer(
            date_checkers=[
                CheckIsBeforeStartOfDay(),
                CheckIsLunchTime(),
                CheckIsDinnerTime(),
                CheckIsPastEndOfDay(),
            ],
            date_transformers=[
                TransformStartOfDay(),
                Transform1Hour(),
                Transform1Hour(),
                TransformNextDay(),
            ],
        )

    def _build_subjects_and_topics(self):

        topic1 = topic("topic 1", "now", dt.timedelta(0))
        subject1 = subject(name="subject 1", topics=[topic1])

        topic2 = topic("topic 2", "now", dt.timedelta(0))
        subject2 = subject(name="subject 2", topics=[topic2])

        return [subject1, subject2]

    def _build_expected_datetimes_1(self):

        return [
            dt.datetime(year=2024, month=6, day=3, hour=9),
            dt.datetime(year=2024, month=6, day=3, hour=10),
            dt.datetime(year=2024, month=6, day=4, hour=10),
            dt.datetime(year=2024, month=6, day=11, hour=10),
            dt.datetime(year=2024, month=7, day=9, hour=10),
            dt.datetime(year=2024, month=10, day=1, hour=10),
            dt.datetime(year=2025, month=3, day=18, hour=10),
        ]

    def _build_expected_datetimes_2(self):

        return [
            dt.datetime(year=2024, month=6, day=3, hour=11),
            dt.datetime(year=2024, month=6, day=3, hour=13),
            dt.datetime(year=2024, month=6, day=4, hour=13),
            dt.datetime(year=2024, month=6, day=11, hour=13),
            dt.datetime(year=2024, month=7, day=9, hour=13),
            dt.datetime(year=2024, month=10, day=1, hour=13),
            dt.datetime(year=2025, month=3, day=18, hour=13),
        ]

    def test_timeline_builder(self):

        # Start on Monday the 3rd of June
        dt_start = dt.datetime(year=2024, month=6, day=3)

        dct_container = self._build_dct_container()

        objTLB = TimeLineBuilder(input_dct_container=dct_container)

        subjects = self._build_subjects_and_topics()

        timeline = objTLB.build_timeline(start_datetime=dt_start, input_subjects=subjects)

        # Should have 2 events for every timestep
        assert len(timeline) == 2 * len(C_DATESTEPS.values())

        # Check the actual values
        expected_dts_1 = self._build_expected_datetimes_1()
        expected_dts_2 = self._build_expected_datetimes_2()

        assert (len(expected_dts_1) + len(expected_dts_2)) == len(timeline)

        for i in range(0, len(expected_dts_1)):

            tl_key = tuple(timeline.keys())[i]

            assert expected_dts_1[i] == timeline[tl_key].cal_datestep.current_datetime
            assert timeline[tl_key].subject == "subject 1"
            assert timeline[tl_key].topic == "topic 1"

        for i in range(len(expected_dts_1), len(expected_dts_2) + len(expected_dts_2)):

            tl_key = tuple(timeline.keys())[i]

            assert (
                expected_dts_2[i - len(expected_dts_1)]
                == timeline[tl_key].cal_datestep.current_datetime
            )
            assert timeline[tl_key].subject == "subject 2"
            assert timeline[tl_key].topic == "topic 2"
