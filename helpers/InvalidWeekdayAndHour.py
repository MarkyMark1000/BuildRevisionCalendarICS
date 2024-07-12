import datetime as dt

class InvalidWeekdayAndHour():

    _data: list

    def __init__(self):

        self._data = list()
        with open('setup_data/Control Files/invalid_weekday_and_time.txt', 'r') as file:
            for line in file:

                line_strip = line.strip()
                line_values = line_strip.split(' ')
                weekday = line_values[0].upper()
                hour = line_values[1]
                hour = hour.split(':')
                hour = int(hour[0])

                wd = 0
                if weekday=="SUNDAY":
                    wd = 6
                elif weekday=="MONDAY":
                    wd=0
                elif weekday=="TUESDAY":
                    wd=1
                elif weekday=="WEDNESDAY":
                    wd=2
                elif weekday=="THURSDAY":
                    wd=3
                elif weekday=="FRIDAY":
                    wd=4
                elif weekday=="SATURDAY":
                    wd=5
                else:
                    raise Exception(f'Invalid weekday: {weekday}')
                
                self._data.append({'weekday': wd, 'hour': hour})

    
    def is_invalid_weekday_and_hour(self, input_datetime: dt) -> bool:

        ret = False
        for row in self._data:
            if input_datetime.weekday() == row['weekday'] and \
                input_datetime.hour == row['hour']:
                ret = True
                break

        return ret
