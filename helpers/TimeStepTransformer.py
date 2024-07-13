import datetime as dt, timedelta

datesteps = {
    '1 day': timedelta(days=1),
    '1 week': timedelta(days=7),
    '1 month': timedelta(days=28),
    '3 month': timedelta(days=84),
    '6 month': timedelta(days=168),
}


class TimeStepTransformer():

    _data: list
    start_datetime: dt.datetime
    end_datetime: dt.datetime

    def __init__(self,
                 start_datetime: dt.datetime,
                 end_datetime: dt.datetime):

        self.start_datetime = start_datetime
        self.end_datetime = end_datetime

    
    def transform(self, input_datetime: dt.datetime, subject: str, topic: str) -> bool:

        if (
            (input_datetime-self.start_datetime).total_second()<0 or
            (self.end_datetime-input_datetime).total_second()<0
            ):
            return None

        current = input_datetime
        ret = {
            input_datetime.strftime('%d-%B-%Y %H'): {
                'datetime': input_datetime,
                'title': subject + ' - ' + topic + ' - start'
            }
        }
        current += timedelta(hours=1)
        ret[current.strftime('%d-%B-%Y %H')] = {
                'datetime': current,
                'title': subject + ' - ' + topic + ' - 1 hour'
        }

        for step_keys, step_values in datesteps.items():

            current += step_values

            if (current-self.end_datetime).total_seconds()>0:
                # gone past the end date, time to leave
                break

            ret[current.strftime('%d-%B-%Y %H')] = {
                'datetime': current,
                'title': subject + ' - ' + topic + ' - ' + step_keys
            }
        
        return ret
