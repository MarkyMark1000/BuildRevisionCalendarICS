import datetime as dt

from .DateCheckers import BaseDateChecker
from .DateTransformers import BaseDateTransformer

"""
Some basic classes for holding the date checkers and
transformers and iterating through them to check if
any conflicts are encountered and then transform the
datetime.
"""


class DCT:
    """Combine a datechecker and date_transfomer to work together."""

    _date_checker: BaseDateChecker
    _date_transformer: BaseDateTransformer

    def __init__(self, date_checker: BaseDateChecker, date_transformer: BaseDateTransformer):

        if not date_checker or not date_transformer:
            raise Exception("must provide date checker and transformer")

        self._date_checker = date_checker
        self._date_transformer = date_transformer

    @property
    def date_checker(self) -> BaseDateChecker:
        """Get date_checker."""
        return self._date_checker

    @property
    def date_transformer(self) -> BaseDateTransformer:
        """Get date_transformer."""
        return self._date_transformer


class DCTContainer:
    """Store list of DCT objects from a list of checkers and transformers.

    Class can load a list of date checkers and transformers into a list
    of DCT objects.   This list can then be used by the transform routine
    to find the next sensible datetime in the calendar timeline.
    """

    _dct_data: list[DCT]

    def __init__(
        self, date_checkers: list[BaseDateChecker], date_transformers: list[BaseDateTransformer]
    ):

        if len(date_checkers) != len(date_transformers):
            raise Exception("date_checkers list must be the smae length as date transformers")

        self._dct_data = list()

        for i in range(0, len(date_checkers)):

            self._dct_data.append(
                DCT(date_checker=date_checkers[i], date_transformer=date_transformers[i])
            )

    def transform(self, input_datetime: dt.datetime) -> dt.datetime:
        """Transform input datetime into the next available time that matches criterea."""
        return_datetime = input_datetime
        i = 0

        while i < len(self._dct_data):

            if self._dct_data[i].date_checker.validate(return_datetime):

                return_datetime = self._dct_data[i]._date_transformer.transform(return_datetime)
                i = 0

            else:

                i += 1

        return return_datetime
