# -*- coding: utf-8 -*-


class BaseError(Exception):
    """
    Baseclass for all Holiday errors.
    """
    pass


class ParseError(BaseError):
    """
    Holiday dates value parse error.
    """


class PeriodRangeError(BaseError):
    """
    Outside the scope of the period error.
    """
