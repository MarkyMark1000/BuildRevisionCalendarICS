from dataclasses import dataclass
import datetime as dt
from .SubjectsAndTopics import subject, topic
import copy
import enum

@dataclass
class CalendarEvent:

    cal_datetime: dt.datetime
    title: str
    time_description: str

    @property
    def timestamp(self):
        return self.cal_datetime.timestamp()

class TimeLineBuilder:

    def build_timeline(self, input_subjects: list[subject]) -> dict[int,CalendarEvent]:

        # copy the input, we are going to reduct/remove items from it
        subjects = copy.deepcopy(input_subjects)

        ret = {}
        current_subject = 0

        while len(subjects) > 0:

            # Get the subject
            subject = subjects[current_subject]





            # If we pass the last subject in the list, switch past it
            if current_subject > len(subjects)-1:
                current_subject = 0
        
        return ret
