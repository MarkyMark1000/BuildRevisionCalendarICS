import datetime as dt
import os

import helpers.DateCheckers as dc
import helpers.DateTransformers as dtf
import helpers.SubjectsAndTopics as st
from helpers.DCTContainer import DCTContainer
from helpers.TimeLine import TimeLineBuilder

C_OUTPUT_DIRECTOR = "./result_data"

def _build_dct_container() -> DCTContainer:
    """setup all of the containers and transformers used by the
    main routine.

    Returns:
        DCTContainer: container for all of our date and time concerns.
    """

    invalid_school_wd_hour = dc.CheckInvalidWeekdayAndHour(
        path="./setup_data/Control Files/invalid_weekday_and_time__school.txt"
    )

    invalid_holiday_wd_hour = dc.CheckInvalidWeekdayAndHour(
        path="./setup_data/Control Files/invalid_weekday_and_time__holiday.txt"
    )

    return DCTContainer(
        date_checkers=[
            dc.CheckIsBeforeStartOfDay(),
            dc.CheckIsLunchTime(),
            dc.CheckIsDinnerTime(),
            dc.CheckIsPastEndOfDay(),
            dc.CheckInvalidDates(path="./setup_data/Control Files/invalid_dates.txt"),
            dc.CheckSchoolTime(
                invalid_weekday_and_hour=invalid_school_wd_hour,
                path="./setup_data/Control Files/school_holidays.txt",
            ),
            dc.CheckSchoolHolidayTime(
                invalid_weekday_and_hour=invalid_holiday_wd_hour,
                path="./setup_data/Control Files/school_holidays.txt",
            ),
        ],
        date_transformers=[
            dtf.TransformStartOfDay(),
            dtf.Transform1Hour(),
            dtf.Transform1Hour(),
            dtf.TransformNextDay(),
            dtf.TransformNextDay(),
            dtf.TransformAfterSchoolOr1Hour(),
            dtf.Transform1Hour(),
        ],
    )


def _build_subjects_and_topics() -> list[st.subject]:

    subject_loader = st.subject_loader()

    subjects_loader = st.subjects_loader(loader=subject_loader)

    subjects_and_topics = subjects_loader.load(directory_path="./setup_data/1Hr Files")

    return subjects_and_topics

def _clear_output_directory():

    breakpoint()
    for filename in os.listdir(C_OUTPUT_DIRECTOR):

        file = os.path.join(C_OUTPUT_DIRECTOR, filename)

        if file.strip()[-3:] != ".md":

            os.remove(file)


def build_calendars(input_datetime: dt.datetime):

    # Build the date checker and transformers.
    dct_container = _build_dct_container()

    # Extract the subjects and topics
    subjects_and_topics = _build_subjects_and_topics()

    # Initiate the timeline builder
    objTLB = TimeLineBuilder(input_dct_container=dct_container)

    # Build the timeline
    timeline = objTLB.build_timeline(
        start_datetime=input_datetime,
        input_subjects=subjects_and_topics
    )

    # Clean output directory and Use the Result Builders to
    _clear_output_directory()

    # output the files

    breakpoint()


if __name__ == "__main__":

    # code to build the calendar
    start_datetime = dt.datetime(year=2024, month=7, day=20, hour=9)

    build_calendars(input_datetime=start_datetime)
