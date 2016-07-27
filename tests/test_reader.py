# -*- coding: utf-8 -*-


from djson.reader import TokenReader
from djson.exc import JSONDecodeError
from djson.consts import Token
import pytest


def _assert(tr, token, value, location):
    assert tr.next_token() == token
    assert tr.token_as_value() == value
    assert tr.location() == location


def test_parse_integer():
    tr = TokenReader("123456,")
    _assert(tr, Token.NUMBER, 123456, "(line: 1, column: 7)")


def test_parse_integer_with_prefix():
    tr = TokenReader("\n+123456:")
    tr.next_token()
    _assert(tr, Token.NUMBER, 123456, "(line: 2, column: 8)")

    tr = TokenReader("-123456 ")
    _assert(tr, Token.NUMBER, -123456, "(line: 1, column: 8)")


def test_parse_float():
    tr = TokenReader("123.456:")
    _assert(tr, Token.NUMBER, 123.456, "(line: 1, column: 8)")


def test_parse_float_with_prefix():
    tr = TokenReader("+123.456,")
    _assert(tr, Token.NUMBER, 123.456, "(line: 1, column: 9)")

    tr = TokenReader("\n-123.456]")
    tr.next_token()
    _assert(tr, Token.NUMBER, -123.456, "(line: 2, column: 9)")


def test_parse_number_failed_with_multi_dot():
    tr = TokenReader("123.45.6}")
    with pytest.raises(JSONDecodeError) as exc_info:
        tr.next_token()

    str_exc_info = str(exc_info)
    assert "(line: 1, column: 7)" in str_exc_info
    assert "found more than one dot character" in str_exc_info


def test_parse_str():
    tr = TokenReader(r'"string"')
    _assert(tr, Token.STRING, "string", "(line: 1, column: 8)")

    tr = TokenReader(r'"stri\\ng"')
    _assert(tr, Token.STRING, r"stri\\ng", "(line: 1, column: 10)")


def test_parse_str_failed_with_multi_line():
    tr = TokenReader('"stri\ng"')
    with pytest.raises(JSONDecodeError) as exc_info:
        tr.next_token()
    str_exc_info = str(exc_info.value)
    assert "(line: 2, column: 0)" in str_exc_info
    assert "donot allow multiple line" in str_exc_info


def test_parse_boolean():
    tr = TokenReader("truefalse")
    _assert(tr, Token.BOOLEAN, True, "(line: 1, column: 4)")
    _assert(tr, Token.BOOLEAN, False, "(line: 1, column: 9)")


def test_parse_boolean_failed():
    tr = TokenReader("treuf")
    with pytest.raises(JSONDecodeError) as exc_info:
        tr.next_token()
    str_exc_info = str(exc_info)
    assert "(line: 1, column: 5)" in str_exc_info
    assert "no boolean value found" in str_exc_info


def test_parse_null():
    tr = TokenReader(":null")
    assert tr.next_token() == Token.SEP_COLON
    _assert(tr, Token.NULL, None, "(line: 1, column: 5)")


def test_parse_null_failed():
    tr = TokenReader("nulL")
    with pytest.raises(JSONDecodeError) as exc_info:
        tr.next_token()
    str_exc_info = str(exc_info.value)
    assert "(line: 1, column: 4)" in str_exc_info
    assert "no null value found" in str_exc_info


def test_parse_characters():
    tr = TokenReader(",:{}[] \n\r")
    tr._token = ""
    location = '(line: 1, column: {0})'
    _assert(tr, Token.SEP_COMMA, "", location.format(1))
    _assert(tr, Token.SEP_COLON, "", location.format(2))
    _assert(tr, Token.OBJECT_BEGIN, "", location.format(3))
    _assert(tr, Token.OBJECT_END, "", location.format(4))
    _assert(tr, Token.ARRAY_BEGIN, "", location.format(5))
    _assert(tr, Token.ARRAY_END, "", location.format(6))
    _assert(tr, Token.EMPTY, "", location.format(7))
    _assert(tr, Token.EMPTY, "", '(line: 2, column: 0)')
    _assert(tr, Token.EMPTY, "", '(line: 3, column: 0)')
