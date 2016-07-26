# -*- coding: utf-8 -*-

from __future__ import absolute_import
import sys


PY3 = sys.version_info >= (3,)

if PY3:
    _unicode_type = str
else:
    _unicode_type = unicode


def to_utf8(value):
    if isinstance(value, bytes):
        return value
    if not isinstance(value, _unicode_type):
        raise TypeError("Expected bytes, unicode, got {0}".format(type(value)))
    return value.encode('utf-8')


def to_unicode(value):
    if isinstance(value, _unicode_type):
        return value
    if not isinstance(value, bytes):
        raise TypeError("Expected bytes, unicode, got {0}".format(type(value)))
    return value.decode('utf-8')
