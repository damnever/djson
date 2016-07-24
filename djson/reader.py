# -*- coding: utf-8 -*-

from __future__ import absolute_import
from collections import deque

from .consts import Token
from .excs import JSONDecodeError, _NoMoreDataError


class TokenReader(object):

    def __init__(self, stream):
        self._data = iter(stream)
        self._buffer = deque()
        self._token = JSONDecodeError("No such token")

    def next_token(self):
        try:
            ch = self._read_next()
        except _NoMoreDataError:
            return Token.JSON_END
        token = Token.ILLEGAL

        if ch == '{':
            token = Token.OBJECT_BEGIN
        elif ch == '}':
            token = Token.OBJECT_END
        elif ch == '[':
            token = Token.ARRAY_BEGIN
        elif ch == ']':
            token = Token.ARRAY_END
        elif ch == '"':
            token = Token.STRING
            self._parse_string()
        elif ch in ('-', '+') or ('0' <= ch <= '9'):
            token = Token.NUMBER
            self._parse_number(ch)
        elif ch in ('t', 'f'):
            token = Token.BOOLEAN
            self._parse_boolean(ch)
        elif ch == 'n':
            token = Token.NULL
            self._parse_null(ch)
        elif ch == ',':
            token = Token.SEP_COMMA
        elif ch == ':':
            token = Token.SEP_COLON
        elif ch in ('\n', '\r', ' ', '\r\n'):
            token = Token.EMPTY

        return token

    def token_as_value(self):
        return self._token

    def _read_next(self):
        if self._buffer:
            return self._buffer.pop()
        try:
            return next(self._data)
        except StopIteration:
            raise _NoMoreDataError()

    def _peek_next(self):
        if self._buffer:
            return self._buffer[-1]
        try:
            ch = next(self._data)
        except StopIteration:
            raise _NoMoreDataError()
        self._buffer.appendleft(ch)
        return ch

    def _parse_number(self, ch):
        nums = [ch]
        sign = 1
        dot_num = 0
        if ch == '-':
            sign = -1

        while 1:
            ch = self._peek_next()
            if not ('0' <= ch <= '9') and ch != '.':
                break
            if ch == '.':
                if dot_num == 0:
                    dot_num += 1
                else:
                    raise JSONDecodeError("parse number error: "
                                          "found more than one dot character.")
            nums.append(ch)
            self._buffer.pop()

        if not nums:
            raise JSONDecodeError("parse number error: no number found.")

        num = ''.join(nums)
        if dot_num:
            self._token = sign * float(num)
        else:
            self._token = sign * int(num)


    def _parse_string(self):
        chs = list()
        slash_num = 0

        while 1:
            ch = self._read_next()
            if ch == '"':
                if slash_num % 2 == 0:
                    break
                slash_num = 0
            elif ch == '\\':
                slash_num += 1
            chs.append(ch)

        if slash_num % 2 != 0:
            raise JSONDecodeError("parse string error: "
                                  "found more than one \"\\\" character.")
        self._token = ''.join(chs)

    def _parse_boolean(self, ch):
        may_true = ch + ''.join(self._read_next() for _ in range(3))
        if may_true == 'true':
            self._token = True
        else:
            may_false = may_true + self._read_next()
            if may_false == 'false':
                self._token = False
            raise JSONDecodeError("parse boolean error: "
                                  "no boolean value found.")

    def _parse_null(self, ch):
        may_null = ch + ''.join(self._read_next() for _ in range(3))
        if may_null == 'null':
            self._token = None
        else:
            raise JSONDecodeError("parse null error: no null value found.")
