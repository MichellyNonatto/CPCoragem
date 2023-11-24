# -*- coding: utf-8 -*-

"""
    holiday
    ~~~~~~~
    :copyright: (c) 2016 by wanshot.
    :license: MIT, see LICENSE for more details.

    SpecialThanks
    ~~~~~~~~~~~~~
    @crohaco: He gave holiday idea to me and he did a review
    @tell-k: He taught me pypi debut way

"""

__version__ = '1.0.0'
__license__ = 'MIT License',
__author__ = 'wanshot'
__author_email__ = 'nishikawa0228@sj9.so-net.ne.jp'


from .core import Holiday
from .exceptions import ParseError, PeriodRangeError
from ._compat import string_types
