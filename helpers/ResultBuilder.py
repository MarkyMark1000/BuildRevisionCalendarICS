import datetime as dt
from abc import ABC, abstractmethod

import pytz
from ics import Calendar, Event  # type: ignore

from .TimeLine import CalendarEvent


class ResultBuilderBase(ABC):
    """Abstract base class for a result builder."""

    _path: str

    def __init__(self, path: str):
        self._path = path

    @property
    def path(self) -> str:
        """Get path to output."""
        return self._path

    @abstractmethod
    def build(self, timeline: dict[int, CalendarEvent]) -> None:
        """Build output from timeline."""
        pass


class ICSResultBuilder(ResultBuilderBase):
    """Build an ICS calendar file from timeline."""

    def _populate_calendar(self, timeline: dict[int, CalendarEvent]) -> Calendar:

        ret = Calendar()

        # Get timeline keys sorted
        sorted_keys = sorted(timeline.keys())

        for unix_dt in sorted_keys:

            # timezone is important for calendar
            dt_temp = timeline[unix_dt].cal_datestep.current_datetime
            dt_temp = dt_temp.replace(tzinfo=pytz.timezone("Europe/London"))

            e = Event()
            e.name = f"{timeline[unix_dt].subject}, {timeline[unix_dt].topic}, {timeline[unix_dt].cal_datestep._datestep}"
            e.begin = dt_temp
            e.duration = dt.timedelta(minutes=50)
            ret.events.add(e)

        return ret

    def build(self, timeline: dict[int, CalendarEvent]) -> None:
        """Build an ICS calendar file from timeline."""
        cal = self._populate_calendar(timeline=timeline)

        cal.events

        with open(self.path, "w") as my_file:
            my_file.writelines(cal.serialize_iter())


class CSVListResultBuilder(ResultBuilderBase):
    """Build a csv file from timeline."""

    def build(self, timeline: dict[int, CalendarEvent]) -> None:
        """Build a csv file from timeline."""
        sorted_keys = sorted(timeline.keys())

        with open(self.path, "w") as my_file:

            for k in sorted_keys:

                cal_event = timeline[k]

                dt = cal_event.cal_datestep.current_datetime
                dt_str = f"{dt:%d %B %Y %H:%M},"

                title_str = (
                    f"{cal_event.subject} - {cal_event.topic} - {cal_event.cal_datestep._datestep}"
                )

                line_str = dt_str + title_str + "\n"

                my_file.write(line_str)
