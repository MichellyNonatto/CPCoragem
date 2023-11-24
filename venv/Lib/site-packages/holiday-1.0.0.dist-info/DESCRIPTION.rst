Judgment whether the holiday

Requiremants
----------------

- Python 2.7 or later.

Install
----------------

.. code-block:: shell

   $ pip install holiday


holiday format
------------------

::

   ('*', '*', '*', '*', '*')
     ┬    ┬    ┬    ┬    ┬
     │    │    │    │    │
     │    │    │    │    │
     │    │    │    │    └─  number of week (1 - 5)
     │    │    │    └─── day of week (1 to 7 or mon to sun)
     │    │    └───── day of month (1 - 31)
     │    └─────── month (1 - 12)
     └───────── year (1 - 9999)

   '*' The asterisk allows all



Usage
----------------


.. code-block:: python

   >>> holiday = Holiday([
   ...     (2016, 1, 1, 'fri', 1),
   ...     (2016, 1, 2, 'sat', 1),
   ... ])

   >>> holiday.is_holiday(date(2016, 1, 1))  # 2016-1-1 Friday 1
   True
   >>> holiday.is_holiday(date(2016, 1, 3))  # 2016-1-3 Sunday 1
   False

- Express all values that can take in the field in asterisk (*)

.. code-block:: python

   >>> holiday = Holiday([
   ...     ('*', 1, 1, 'fri', 1),
   ...     ('*', 1, 1, 'thu', 1),
   ... ])

   >>> holiday.is_holiday(date(2016, 1, 1))  # 2016-1-1 Friday 1
   True
   >>> holiday.is_holiday(date(2015, 1, 1))  # 2015-1-1 Thursday 1
   True
   >>> holiday.is_holiday(date(2014, 1, 1))  # 2014-1-1 Wednesday 1
   False

- is_business_day() returns the inverse of the truth-value of the is_holiday()

.. code-block:: python

    >>> holiday = Holiday([
    ...     ('*', '*', '*', '*', '*'),
    ... ])

    >>> holiday.is_holiday(date(2016, 1, 1))  # 2016-1-1 Friday 1
    True
    >>> holiday.is_business_day(date(2016, 1, 1))  # 2016-1-1 Friday 1
    False

License
--------

This software is released under the MIT License, see LICENSE.txt.


