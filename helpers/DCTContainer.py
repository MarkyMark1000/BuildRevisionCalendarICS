import datetime as dt

from .DateCheckers import BaseDateChecker
from .DateTransformers import BaseDateTransformer

"""
Some basic classes for holding the date checkers and
transformers and iterating through them to check if
any conflicts are encountered and then transform the
datetime.
"""

class DCT():

    _date_checker: BaseDateChecker
    _date_transformer: BaseDateTransformer

    def __init__(self,
                 date_checker: BaseDateChecker,
                 date_transformer: BaseDateTransformer):
        
        if not date_checker or not date_transformer:
            raise Exception("must provide date checker and transformer")
        
        self._date_checker = date_checker
        self._date_transformer = date_transformer
    
    @property
    def date_checker(self):
        return self._date_checker
    
    @property
    def date_transformer(self):
        return self._date_transformer

class DCTContainer():
    """
    Class where we can load up a list of date checkers and containers and
    then use the transform feature to find the next appropriate date that
    doesn't conflict with any of the conditions added in the list.
    see test_dct_container for a basic example.
    """
    _dct_data: list

    def __init__(self,
                 date_checkers: list,
                 date_transformers: list):

        if len(date_checkers) != len(date_transformers):
            raise Exception('date_checkers list must be the smae length as date transformers')
        
        self._dct_data = list()

        for i in range(0, len(date_checkers)):

            self._dct_data.append(
                DCT(
                    date_checker = date_checkers[i],
                    date_transformer=date_transformers[i]
                )
            )
    
    def transform(self, input_datetime: dt.datetime) -> dt.datetime:

        return_datetime = input_datetime
        i = 0

        while i<len(self._dct_data):

            if self._dct_data[i].date_checker.validate(return_datetime):

                return_datetime = \
                    self._dct_data[i]._date_transformer.transform(return_datetime)
                i=0

            else:

                i+=1
        
        return return_datetime
