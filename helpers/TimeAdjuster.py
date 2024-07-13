import datetime as dt
from .InvalidDates import InvalidDates
from .SchoolHolidays import SchoolHolidays
from .InvalidWeekdayAndHour import InvalidWeekdayAndHour

class TimeAdjuster():

    logging: bool = False
    invalid_dates: InvalidDates
    school_holidays: SchoolHolidays
    invalid_weekday_and_hour: InvalidWeekdayAndHour

    def __init__(self,
                 invalid_dates: InvalidDates,
                 school_holidays: SchoolHolidays,
                 invalid_weekday_and_hour: InvalidWeekdayAndHour):
        
        self.invalid_dates = invalid_dates
        self.school_holidays = school_holidays
        self.invalid_weekday_and_hour = invalid_weekday_and_hour
        if self.logging:
            print('\n')
    
    def _log(self, title: str, input_datetime: dt.datetime) -> None:
        if self.logging:
            print(title + ':   ',input_datetime.strftime('%d-%m-%Y %H'), '\n')

    def validate_or_find_next(self, input_datetime: dt.datetime) -> dt.datetime:
        '''
        This is a recursive process that returns the input_datetime if it
        doesn't confict with any of our conditions.   Otherwise it is
        called recursivley to find a date in the future that doesn't clash.
        It deals with the following:
            - lunch and dinner
            - invalid weekday and hours (setup data)
            - invalid dates (setup data)
            - school holidays and weekends (9am to 8pm)
            - normal school days (6pm to 8pm)
        '''
        # breakpoint()    # year=2024, month=7, day=10, hour=18

        if input_datetime.hour == 12 or input_datetime.hour == 17:
            # It's lunchtime, we need a break
            new_time = input_datetime + dt.timedelta(hours=1)
            self._log('1', new_time)
            result = self.validate_or_find_next(new_time)
            return result
        elif self.invalid_weekday_and_hour.is_invalid_weekday_and_hour(input_datetime):
            # It's an invalid weekday and hour, so add one hour and try again
            new_time = input_datetime + dt.timedelta(hours=1)
            self._log('2', new_time)
            result = self.validate_or_find_next(new_time)
            return result
        elif self.invalid_dates.is_invalid_date(input_datetime):
            # Invalid date, so add one day and move to start of day, then try again
            new_time = (input_datetime + dt.timedelta(days=1)).replace(hour=9, minute=0)
            self._log('3', new_time)
            result = self.validate_or_find_next(new_time)
            return result
        elif (
                self.school_holidays.is_within_school_holiday(input_datetime) or
                input_datetime.weekday() in (5,6)
            ):
            # Treat school holidays and weekends the same
            if input_datetime.hour > 20:
                new_time = (input_datetime + dt.timedelta(days=1)).replace(hour=9, minute=0)
                self._log('4', new_time)
                result = self.validate_or_find_next(new_time)
                return result
        else:
            # School day
            if input_datetime.hour < 18:
                # During school day, so move to 6pm
                new_time = input_datetime + dt.timedelta(hours=(18-input_datetime.hour))
                self._log('5', new_time)
                result = self.validate_or_find_next(new_time)
                return result
            elif input_datetime.hour > 20:
                # After 8pm so move to the next day
                new_time = (input_datetime + dt.timedelta(days=1)).replace(hour=9, minute=0)
                self._log('6', new_time)
                result = self.validate_or_find_next(new_time)                
                return result
        
        return input_datetime

