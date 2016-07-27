# -*- coding: utf-8 -*-

import os

from djson.decoder import JSONDecoder, load, loads
from djson.reader import TokenReader
from djson.exc import JSONDecodeError
from djson.consts import State
import pytest


def _raises(s, column, err_msg, expect_state):
    location = '(line: 1, column: {0})'.format(column)
    decoder = JSONDecoder(TokenReader(s))
    with pytest.raises(JSONDecodeError) as exc_info:
        decoder.parse()
    str_exc_info = str(exc_info.value)
    assert location in str_exc_info
    assert err_msg in str_exc_info
    assert decoder._state.has(expect_state)


def test_decode_failed_with_unexpect_opening_brace():
    err_msg = '{'

    _raises(r'{"1"{: 2}', 5, err_msg, State.EXPECT_COLON)
    _raises(r'{{1: 2}', 2, err_msg,
            State.EXPECT_KEY | State.EXPECT_OBJECT_END)
    _raises(r'{1: 2{}', 6, err_msg,
            State.EXPECT_COMMA | State.EXPECT_OBJECT_END)
    _raises(r'{1: ["2"{]}', 9, err_msg,
            State.EXPECT_COMMA | State.EXPECT_ARRAY_END)
    _raises(r'{1: [2]{}', 8, err_msg, State.EXPECT_COMMA)


def test_decode_failed_with_unexpect_closing_brace():
    err_msg = '}'

    _raises(r'{"1"}', 5, err_msg, State.EXPECT_COLON)
    _raises(r'{1:}}', 4, err_msg, State.EXPECT_VALUE)
    _raises(r'{1:"2",[}}', 9,
            err_msg, State.EXPECT_VALUE | State.EXPECT_ARRAY_END)
    _raises(r'{"1": [[}', 9, err_msg,
            State.EXPECT_VALUE | State.EXPECT_ARRAY_END)


def test_decode_failed_with_unexpect_opening_bracket():
    err_msg = '['

    _raises(r'{[}', 2, err_msg, State.EXPECT_KEY | State.EXPECT_OBJECT_END)
    _raises(r'{"1": 2[}', 8, err_msg, State.EXPECT_COMMA)


def test_decode_failed_with_unexpect_closing_bracket():
    err_msg = ']'

    _raises(r'{]}', 2, err_msg, State.EXPECT_KEY | State.EXPECT_OBJECT_END)
    _raises(r'{"1": ]}', 7, err_msg, State.EXPECT_VALUE)
    _raises(r'{"1": []]}', 9, err_msg, State.EXPECT_COMMA)


def test_decode_failed_with_unexpect_string():
    _raises(r'"name"{', 1, "name", State.EXPECT_OBJECT_BEGIN)
    _raises(r'{"1": 2"name"', 8, "name",
            State.EXPECT_COMMA | State.EXPECT_OBJECT_END)
    _raises(r'{"1": [1]"name"', 10, "name",
            State.EXPECT_COMMA | State.EXPECT_OBJECT_END)


def test_decode_failed_with_unexpect_integer():
    _raises(r'1{', 1, "1", State.EXPECT_OBJECT_BEGIN)
    _raises(r'{"1": "name"3,', 13, "3",
            State.EXPECT_COMMA | State.EXPECT_OBJECT_END)


def test_decode_failed_with_unexpect_boolean():
    _raises(r'true{', 1, "true", State.EXPECT_OBJECT_BEGIN)
    _raises(r'{"1": "name"false', 13, "false",
            State.EXPECT_COMMA | State.EXPECT_OBJECT_END)


def test_decode_failed_with_unexpect_null():
    _raises(r'null{', 1, "null", State.EXPECT_OBJECT_BEGIN)
    _raises(r'{"1": "name"null', 13, "null",
            State.EXPECT_COMMA | State.EXPECT_OBJECT_END)


def test_decode_failed_with_unexpect_colon():
    _raises(r'{:1}', 2, ",", State.EXPECT_KEY | State.EXPECT_OBJECT_END)
    _raises(r'{"2":1:}', 7, ",",
            State.EXPECT_COMMA | State.EXPECT_OBJECT_END)
    _raises(r'{"2":[:}', 7, ",", State.EXPECT_VALUE | State.EXPECT_ARRAY_END)


def test_decode_failed_with_unexpect_comma():
    _raises(r'{,1}', 2, ",", State.EXPECT_KEY | State.EXPECT_OBJECT_END)
    _raises(r'{"2":,}', 6, ",", State.EXPECT_VALUE)
    _raises(r'{"2":[,}', 7, ",", State.EXPECT_VALUE | State.EXPECT_ARRAY_END)


def test_decode_failed_with_unexpect_redundant_data():
    _raises(r'{}"1"', 5, '1', State.EXPECT_JSON_END)


def _compare_list(l1, l2):
    for item1, item2 in zip(sorted(l1), sorted(l2)):
        if isinstance(item1, list):
            assert isinstance(item2, list)
            _compare_list(item1, item2)
        elif isinstance(item1, dict):
            assert isinstance(item2, dict)
            _compare_dict(item1, item2)
        else:
            assert item1 == item2


def _compare_dict(d1, d2):
    for k1 in d1:
        assert k1 in d2
        v1 = d1[k1]
        v2 = d2[k1]
        if isinstance(v1, list):
            assert isinstance(v2, list)
        elif isinstance(v1, dict):
            assert isinstance(v2, dict)
            _compare_dict(v1, v2)
        else:
            assert v1 == v2


target = {
    "name": "damnever",
    "age": [21, 22],
    21: True,
    22: False,
    None: "null",
    True: {
        "www": "github",
    },
    "negative": -123.456,
}


JSON_STR = r"""
{
    "name": "damnever",
    "age": [21, 22],
    21: true,
    22: false,
    null: "null",
    true: {
        "www": "github",
    },
    "negative": -123.456,
}
"""


def test_loads():
    data = loads(JSON_STR)
    _compare_dict(target, data)


def test_load():
    path = os.path.join(os.path.dirname(__file__), 'data.txt')
    with open(path, 'rb') as f:
        data = load(f)
    _compare_dict(target, data)
