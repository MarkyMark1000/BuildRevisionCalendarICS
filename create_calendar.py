import datetime as dt
import os

import helpers.DateCheckers as dc
import helpers.DateTransformers as dtf
import helpers.ResultBuilder as rb
import helpers.SubjectsAndTopics as st
from helpers.DCTContainer import DCTContainer
from helpers.TimeLine import CalendarEvent, TimeLineBuilder

C_OUTPUT_DIRECTOR = "./result_data"


def _build_dct_container() -> DCTContainer:
    """Setup DCTContainer.

    Initiate all of the containers and transformers used by the
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


def _clear_output_directory() -> None:

    for filename in os.listdir(C_OUTPUT_DIRECTOR):

        file = os.path.join(C_OUTPUT_DIRECTOR, filename)

        if file.strip()[-3:] != ".md":

            os.remove(file)


def _output_result_data(input_timeline: dict[int, CalendarEvent]) -> None:

    ics_rb = rb.ICSResultBuilder(path=C_OUTPUT_DIRECTOR + "/output_calendar.ics")
    ics_rb.build(timeline=input_timeline)

    csv_rb = rb.CSVListResultBuilder(path=C_OUTPUT_DIRECTOR + "/output_data.csv")
    csv_rb.build(timeline=input_timeline)


def build_calendars(input_datetime: dt.datetime) -> None:
    """Build calendar results.

    This is the main routine that builds the calendar output files within the
    /result_data/ directory.   It uses the code within the /helpers/ directory
    and the files within the /setup_data/ directory.

    Args:
        input_datetime (dt.datetime): start date of when to build calendar from.
    """
    # Build the date checker and transformers.
    dct_container = _build_dct_container()

    # Extract the subjects and topics
    subjects_and_topics = _build_subjects_and_topics()

    # Initiate the timeline builder
    objTLB = TimeLineBuilder(input_dct_container=dct_container)

    # Build the timeline
    timeline = objTLB.build_timeline(
        start_datetime=input_datetime, input_subjects=subjects_and_topics
    )

    # Clean output directory and Use the Result Builders to
    _clear_output_directory()

    # output the files
    _output_result_data(input_timeline=timeline)

    print("-" * 15)
    print("Finished - check result_data directory!")
    print("-" * 15)


if __name__ == "__main__":

    # code to build the calendar
    start_datetime = dt.datetime(year=2024, month=7, day=20, hour=9)

    build_calendars(input_datetime=start_datetime)
