import datetime as dt

class SchoolHolidays():

    _data: list

    def __init__(self):

        self._data = list()
        with open('setup_data/Control Files/school_holidays.txt', 'r') as file:
            for line in file:
                rdata = line.split(',')
                start_date = rdata[0].strip()
                end_date = rdata[1].strip()
                start_date = dt.datetime.strptime(start_date, '%d-%B-%Y')
                end_date = dt.datetime.strptime(end_date, '%d-%B-%Y')
                self._data.append({'start_date': start_date, 'end_date': end_date})
        
        # print('\n')
        # print(self._data)

    
    def is_within_school_holiday(self, input_datetime: dt) -> bool:

        ret = False
        for row in self._data:
            if (input_datetime-row['start_date']).total_seconds() >= 0 and \
                (input_datetime-row['start_date']).total_seconds() <= \
                (row['end_date']-row['start_date']).total_seconds():
            
                ret = True
                break

        return ret
