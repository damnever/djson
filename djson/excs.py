# -*- coding: utf-8 -*-

from __future__ import absolute_import


class JSONDecodeError(Exception):
    pass


class JSONEncodeError(Exception):
    pass


class _NoMoreDataError(Exception):
    pass
