# -*- coding: utf-8 -*-

from __future__ import absolute_import


# tokens
class Token(object):
    ILLEGAL = 0
    OBJECT_BEGIN = 1
    OBJECT_END = 2
    ARRAY_BEGIN = 3
    ARRAY_END = 4
    STRING = 5
    SEP_COMMA = 6
    SEP_COLON = 7
    NUMBER = 8
    BOOLEAN = 9
    NULL = 10
    EMPTY = 11
    JSON_END = 12


# states
class State(object):
    EXPECT_OBJECT_BEGIN = 1 << 0
    EXPECT_OBJECT_END = 1 << 1
    EXPECT_ARRAY_BEGIN = 1 << 2
    EXPECT_ARRAY_END = 1 << 3
    EXPECT_STRING = 1 << 4
    EXPECT_NUMBER = 1 << 5
    EXPECT_BOOLEAN = 1 << 6
    EXPECT_NULL = 1 << 7
    EXPECT_COMMA = 1 << 8
    EXPECT_COLON = 1 << 9
    EXPECT_JSON_END = 1 << 10
    EXPECT_KEY = (EXPECT_STRING |
                  EXPECT_NUMBER |
                  EXPECT_BOOLEAN |
                  EXPECT_NULL)
    EXPECT_VALUE = (EXPECT_OBJECT_BEGIN |
                    EXPECT_ARRAY_BEGIN |
                    EXPECT_KEY)

    def __init__(self, state):
        self._current_state = state

    def reset(self, state):
        self._current_state = state

    def has(self, state):
        return self._current_state & state
