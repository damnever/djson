# -*- coding: utf-8 -*-

from __future__ import absolute_import
from collections import deque

from .consts import Token
from .exc import JSONDecodeError, _NoMoreDataError


class TokenReader(object):

    def __init__(self, stream):
        self._data = iter(stream)
        self._buffer = deque()
        self._token = JSONDecodeError("No such token")
        self._line = 1
        self._column = 0

    def location(self, offset=0):
        return "(line: {0}, column: {1})".format(
            self._line, self._column-offset)

    def next_token(self, _empty_chs={'\n', '\r', ' ', '\t', '\f', '\b'}):
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
        elif ch in _empty_chs:
            token = Token.EMPTY

        return token

    def token_as_value(self):
        return self._token

    def _next_char(self, _line_seps={'\n', '\r'}):
        try:
            ch = next(self._data)
        except StopIteration:
            raise _NoMoreDataError()
        if ch in _line_seps:
            self._line += 1
            self._column = 0
        else:
            self._column += 1
        return ch

    def _read_next(self):
        if self._buffer:
            return self._buffer.pop()
        return self._next_char()

    def _peek_next(self):
        if self._buffer:
            return self._buffer[-1]
        ch = self._next_char()
        self._buffer.appendleft(ch)
        return ch

    def _parse_number(self, ch):
        nums = [ch]
        dot_num = 0

        while 1:
            ch = self._peek_next()
            if not ('0' <= ch <= '9') and ch != '.':
                break
            if ch == '.':
                if dot_num != 0:
                    raise JSONDecodeError(
                        "parse number error in {0}: found more than one dot"
                        " character.".format(self.location())
                    )
                dot_num += 1
            nums.append(ch)
            self._buffer.pop()

        num = ''.join(nums)
        if dot_num:
            self._token = float(num)
        else:
            self._token = int(num)

    def _parse_string(self, _illegal_chs={'\n', '\r', '\t', '\f', '\b'}):
        chs = list()

        while 1:
            ch = self._read_next()
            if ch in _illegal_chs:
                raise JSONDecodeError(
                    "parse string error in {0}: donot allow"
                    " multiple line.".format(self.location())
                )
            if ch == '"':
                break
            chs.append(ch)

        self._token = ''.join(chs)

    def _parse_boolean(self, ch):
        may_true = ch + ''.join(self._read_next() for _ in range(3))
        if may_true == 'true':
            self._token = True
        else:
            may_false = may_true + self._read_next()
            if may_false == 'false':
                self._token = False
            else:
                raise JSONDecodeError(
                    "parse boolean error in {0}: no boolean"
                    " value found.".format(self.location())
                )

    def _parse_null(self, ch):
        may_null = ch + ''.join(self._read_next() for _ in range(3))
        if may_null == 'null':
            self._token = None
        else:
            raise JSONDecodeError(
                "parse null error in {0}: no null"
                " value found.".format(self.location())
            )
