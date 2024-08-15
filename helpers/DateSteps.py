import datetime as dt

# ORDER OF KEYS IS IMPORTANT - ASCENDING
C_DATESTEPS = {
    "now": dt.timedelta(0),
    "1 hour": dt.timedelta(hours=1),
    "1 day": dt.timedelta(days=1),
    "1 week": dt.timedelta(days=7),
    "1 month": dt.timedelta(days=28),
    "3 month": dt.timedelta(days=84),
    "6 month": dt.timedelta(days=168),
}


class datestep:
    """Represents a datetime and it's position in the C_DATESTEPS dictionary."""

    _current_datetime: dt.datetime
    _datestep: str

    def __init__(self, input_datetime: dt.datetime, current_step: str = None):

        if not current_step:
            # default to now
            self._datestep = tuple(C_DATESTEPS.keys())[0]
        elif current_step not in C_DATESTEPS.keys():
            raise Exception(f"Invalid datestep key: {current_step}")
        else:
            self._datestep = current_step

        self._current_datetime = input_datetime

    @property
    def timedelta(self):
        """Get timedelta for datestep."""
        return C_DATESTEPS[self._datestep]

    @property
    def current_datetime(self):
        """Get current datetime."""
        return self._current_datetime

    @current_datetime.setter
    def current_datetime(self, new_datetime: dt.datetime):
        # We will need to be able to adjust this based upon
        # calendar conflicts etc
        self._current_datetime = new_datetime

    def get_next_datestep(self):
        """Get the next datestep after this datestep using C_DATESTEPS."""
        index = tuple(C_DATESTEPS.keys()).index(self._datestep)
        if index >= len(C_DATESTEPS.keys()) - 1:
            return None
        else:
            new_key = tuple(C_DATESTEPS.keys())[index + 1]
            time_delta = C_DATESTEPS[new_key]
            new_datetime = self._current_datetime + time_delta
            return datestep(input_datetime=new_datetime, current_step=new_key)
