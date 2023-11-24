# -*- coding: utf-8 -*-
from __future__ import absolute_import
from collections import (
    defaultdict,
    OrderedDict,
)
from itertools import product

from .exceptions import (
    ParseError,
    PeriodRangeError
)
from ._compat import string_types


WEEK_MAP = OrderedDict((
    ("mon", 1),
    ("tue", 2),
    ("wed", 3),
    ("thu", 4),
    ("fri", 5),
    ("sat", 6),
    ("sun", 7),
))

ORDER_WEEK = WEEK_MAP.keys()

TIME_INFO = OrderedDict((
    ("year", (1, 9999)),
    ("month", (1, 12)),
    ("day", (1, 31)),
    ("day_of_week", (1, 7)),
    ("num_of_week", (1, 6)),
))

TIME_LABEL = TIME_INFO.keys()


class Holiday(object):
    """
    Base class
    """

    def __init__(self, times):
        """
        :param tuple of list times: plz see below
        """
        # ('*', '*', '*', '*', '*')
        #   ┬    ┬    ┬    ┬    ┬
        #   │    │    │    │    │
        #   │    │    │    │    │
        #   │    │    │    │    └─  number of week (1 - 5)
        #   │    │    │    └─── day of week (1 to 7 or mon to sun)
        #   │    │    └───── day of month (1 - 31)
        #   │    └─────── month (1 - 12)
        #   └───────── year (1 - 9999)

        self._check_holiday_structure(times)

        self.year = defaultdict(set)
        self.month = defaultdict(set)
        self.day = defaultdict(set)
        self.day_of_week = defaultdict(set)
        self.num_of_week = defaultdict(set)

        for idx, (year, month, day, day_of_week, num_of_week) in enumerate(times):
            if isinstance(day_of_week, string_types):
                day_of_week = WEEK_MAP.get(day_of_week, "*")
            self.year[year].add(idx)
            self.month[month].add(idx)
            self.day[day].add(idx)
            self.day_of_week[day_of_week].add(idx)
            self.num_of_week[num_of_week].add(idx)

    def _check_holiday_structure(self, times):
        """ To check the structure of the HolidayClass

        :param list times: years or months or days or number week
        :rtype: None or Exception
        :return: in the case of exception returns the exception
        """

        if not isinstance(times, list):
            raise TypeError("an list is required")

        for time in times:
            if not isinstance(time, tuple):
                raise TypeError("a tuple is required")
            if len(time) > 5:
                raise TypeError("Target time takes at most 5 arguments"
                                " ('%d' given)" % len(time))
            if len(time) < 5:
                raise TypeError("Required argument '%s' (pos '%d')"
                                " not found" % (TIME_LABEL[len(time)], len(time)))

            self._check_time_format(TIME_LABEL, time)

    def _check_time_format(self, labels, values):
        """ To check the format of the times

        :param list labels: years or months or days or number week
        :param list values: number or the asterisk in the list
        :rtype: None or Exception
        :raises PeriodRangeError: outside the scope of the period
        :raises ParseError: not parse the day of the week
        :return: in the case of exception returns the exception
        """

        for label, value in zip(labels, values):
            if value == "*":
                continue
            if label == "day_of_week":
                if isinstance(value, string_types):
                    if value not in ORDER_WEEK:
                        raise ParseError("'%s' is not day of the week. "
                                         "character is the only '%s'" % (
                                             value, ', '.join(ORDER_WEEK)))
                elif not isinstance(value, int):
                    raise TypeError("'%s' is not an int" % value)

            if label in ["year", "month", "day", "num_of_week"]:
                if not isinstance(value, int):
                    raise TypeError("'%s' is not an int" % value)

            if isinstance(value, int):
                start, end = TIME_INFO[label]
                if not start <= value <= end:
                    raise PeriodRangeError("'%d' is outside the scope of the period "
                                           "'%s' range: '%d' to '%d'" % (
                                               value, label, start, end))

    def is_holiday(self, date):
        """ Whether holiday judges

        :param datetime date: datetime.date object
        :rtype: bool
        """
        time = [
            date.year,
            date.month,
            date.day,
            date.isoweekday(),
            _extract_week_number(date)
        ]

        target = []
        for key, data in list(zip(TIME_LABEL, time)):
            d = getattr(self, key)
            asterisk = d.get("*", set())
            s = asterisk.union(d.get(data, set()))
            target.append(list(s))

        for result in map(set, product(*target)):
            if len(result) == 1:
                return True
        return False

    def is_business_day(self, date):
        """ Whether the business day

        :rtype: bool
        """
        return not(self.is_holiday(date))


def _extract_week_number(date):
    first_date = date.replace(day=1)
    return int(date.strftime('%W')) - int(first_date.strftime('%W')) + 1
