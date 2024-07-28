from dataclasses import dataclass
import datetime as dt
from .SubjectsAndTopics import subject, topic
from .DCTContainer import DCTContainer
from .DateSteps import datestep
import copy

@dataclass
class CalendarEvent:

    cal_datestep: datestep
    subject: str
    topic: str

class TimeLineBuilder:

    _dct_container: DCTContainer

    def __init__(self, input_dct_container: DCTContainer):

        self._dct_container = input_dct_container

    def _find_next_datetime_if_necessary(self, current_timeline: dict, input_datetime) -> dt.datetime:

        next_dt = self._dct_container.transform(input_datetime=next_dt)

        while int(next_dt.timestamp()) in current_timeline.keys():
            next_dt = input_datetime + dt.timedelta(hours=1)
            next_dt = self._dct_container.transform(input_datetime=next_dt)
        
        return next_dt

    def _get_topics_for_timeline(self, current_timeline: dict,
                                       subject: subject, topic: topic,
                                       start_datetime: dt.datetime) -> dict[CalendarEvent]:

        ret = {}

        # Populate the first item on the timeline
        cur_time = start_datetime
        cur_datestep = datestep(
            input_datetime = start_datetime,
            current_step = topic.timedelta_key
        )
        cur_calendar = CalendarEvent(
            cal_datestep = cur_datestep,
            subject = subject.name,
            topic = topic.description
        )
        ret[int(cur_calendar.cal_datestep.current_datetime.timestamp())] = cur_calendar

        # Populate remaining items on the timeline
        while cur_datestep is not None:

            cur_datestep = cur_datestep.get_next_datestep()
            next_time = self._find_next_datetime_if_necessary(current_timeline=current_timeline,
                                                              input_datetime=cur_datestep.current_datetime)
            cur_datestep.current_datetime = next_time

            cur_calendar = CalendarEvent(
                cal_datestep = cur_datestep,
                subject = subject.name,
                topic = topic.description
            )
            ret[int(cur_calendar.cal_datestep.current_datetime.timestamp())] = cur_calendar

        return ret

    def build_timeline(self,
                       start_datetime: dt.datetime,
                       input_subjects: list[subject]) -> dict[int,CalendarEvent]:

        # copy the input, we are going to reduct/remove items from it
        subjects = copy.deepcopy(input_subjects)

        ret = {}
        current_subject = 0
        current_datetime = start_datetime

        while len(subjects) > 0:

            # Get the subject
            subject = subjects[current_subject]

            # Get the topic
            topic = subject.topics[subject.current_topic]

            # Add the topic into a timeline, then add it to ret
            timeline = self._get_topics_for_timeline(self, 
                                                    current_timeline=ret,
                                                    subject=subject,
                                                    topic=topic,
                                                    start_datetime=current_datetime)
            ret.update(timeline)
            
            # Move the current subject onto the next topic
            subjects[current_subject].current_topic += 1

            # If we exceed the number of topics, remove the
            # subject from the list, otherwise move current
            # subject onto the next subject
            if subjects[current_subject].current_topic >= len(subject.topics):
                subjects.pop(current_subject)
            else:
                current_subject += 1
                if current_subject >= len(subjects):
                    current_subject = 0
            
            # Find the next datetime to start adding calendar events
            current_datetime = current_datetime + dt.timedelta(hours=1)
            current_datetime = self._find_next_datetime_if_necessary(current_timeline=ret,
                                                                    input_datetime=current_datetime)
        
        return ret
