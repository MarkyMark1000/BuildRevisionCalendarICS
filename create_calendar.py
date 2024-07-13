from ics import Calendar, Event

from helpers.FileLoader import load_files
from helpers.TimeAdjuster import TimeAdjuster
from helpers.SchoolHolidays import SchoolHolidays
from helpers.InvalidDates import InvalidDates
from helpers.InvalidWeekdayAndHour import InvalidWeekdayAndHour

from datetime import timedelta, datetime
import pytz

datesteps = {
    '1 day': timedelta(days=1),
    '1 week': timedelta(days=7),
    '1 month': timedelta(days=28),
    '3 month': timedelta(days=84),
    '6 month': timedelta(days=168),
}

objSH = SchoolHolidays()
objID = InvalidDates()
objIWH = InvalidWeekdayAndHour()
objTimeAdjuster = TimeAdjuster(
    invalid_dates=objID,
    school_holidays=objSH,
    invalid_weekday_and_hour=objIWH
)

def _validate_or_find_next_hour(ret: dict, input_datetime: datetime) -> datetime:

    # if the input datetime is in the ret dictionary already or its adjusted
    # by the time adjuster, process it here
    key_datetime = objTimeAdjuster.validate_or_find_next(input_datetime=input_datetime)
    if int(key_datetime.timestamp()) in ret.keys():
        # It already exists, add an hour and try again
        key_datetime += timedelta(hours=1)
        key_datetime = _validate_or_find_next_hour(ret, key_datetime)
    
    return key_datetime


def build_basic_topic_dictionary(ret: dict, start_datetime: datetime, subject: str, topic: str) -> dict:

    next_dt = start_datetime
    next_dt = _validate_or_find_next_hour(ret, next_dt)
    ret[int(next_dt.timestamp())] = {
        'title': subject + ',  ' + topic + ',  Start',
        'dt': next_dt
    }
    print(int(next_dt.timestamp()), ', ', next_dt, subject + ',  ' + topic + ',  Start')
    # Always add 1 hour no matter what
    next_dt += timedelta(hours=1)
    next_dt = _validate_or_find_next_hour(ret, next_dt)
    ret[int(next_dt.timestamp())] = {
        'title': subject + ',  ' + topic + ',  1 Hr',
        'dt': next_dt
    }
    print(int(next_dt.timestamp()), ', ', next_dt, subject + ',  ' + topic + ',  1 Hr')

    for k,v in datesteps.items():

        next_dt += v
        next_dt = _validate_or_find_next_hour(ret, next_dt)
        ret[int(next_dt.timestamp())] = {
            'title': subject + ',  ' + topic + ',  ' + k,
            'dt': next_dt
        }
        print(int(next_dt.timestamp()), ', ', next_dt, subject + ',  ' + topic + ',  ' + k)

    return ret


def build_calendar(start_datetime: datetime):

    print('\n')
    print('-'*15)
    print('START')
    print('-'*15)

    data = load_files()

    ret = {}
    current_dt = start_datetime

    # Need a way to add this subject1-topic1, subject2-topic1, ...
    # subject1-topic2, subject2-topic2, ... etc

    control = {s:0 for s in data.keys()}

    subject_no = 0

    while control:

        # bit rubbish, sort out later
        subject = [str(k) for k in control.keys()][subject_no]
        topic_row = control[subject]
        actual_topic = data[subject][topic_row]

        build_basic_topic_dictionary(ret,
                                    current_dt,
                                    subject=subject,
                                    topic=actual_topic)

        current_dt = _validate_or_find_next_hour(ret, current_dt)

        control[subject]+=1

        if control[subject]>len(data[subject])-1:
            # We have finished the subject, so remove from the data and control
            control.pop(subject)
            data.pop(subject)
        subject_no += 1
        if subject_no > len(control.keys())-1:
            subject_no = 0
        
        # print('sub: ', subject_no, 'keys: ', control.keys())

    # Add to the calendar
    c = Calendar()
    sorted_keys = sorted(ret.keys())
    for k in sorted_keys:

        dt_temp = ret[k]['dt']
        dt_temp = dt_temp.replace(tzinfo=pytz.timezone('Europe/London'))

        e = Event()
        e.name = ret[k]['title']
        e.begin = dt_temp
        e.duration = timedelta(minutes=50)
        c.events.add(e)

    c.events

    with open('revision_timetable.ics', 'w') as my_file:
        my_file.writelines(c.serialize_iter())



if __name__ == "__main__":

    # code to build the calendar 

    start_datetime = datetime(year=2024, month=7, day=14, hour=9)

    build_calendar(start_datetime)