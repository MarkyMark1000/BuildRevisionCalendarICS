import datetime as dt

class InvalidDates():

    _data: list

    def __init__(self, path='setup_data/Control Files/invalid_dates.txt'):

        self._data = list()
        with open(path, 'r') as file:
            for line in file:

                date_value = line.strip()
                date_value = dt.datetime.strptime(date_value, '%d-%B-%Y')
                self._data.append(date_value)

    
    def is_invalid_date(self, input_datetime: dt) -> bool:

        ret = False
        for row in self._data:
            if input_datetime.date() == row.date():
                ret = True
                break

        return ret
