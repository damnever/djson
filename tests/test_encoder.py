# -*- coding: utf-8 -*-

import pytest
from djson.encoder import JSONEncoder


@pytest.fixture(scope='module')
def encoder():
    return JSONEncoder(None)


def test_encode_none(encoder):
    assert encoder.encode_NoneType(None) == 'null'


def test_encode_number(encoder):
    ni = 123325
    nf = 123.456
    assert encoder.encode_int(ni) == '{0}'.format(ni)
    assert encoder.encode_float(nf) == '{0}'.format(nf)


def test_encode_bool(encoder):
    assert encoder.encode_bool(True) == 'true'
    assert encoder.encode_bool(False) == 'false'


def test_encode_str(encoder):
    s = "12334324324"
    assert encoder.encode_str(s) == '"{0}"'.format(s)


def test_encode_list(encoder):
    lobj = [1, 2.4, "qwer", '34', -456, True, None, False]
    assert encoder.encode_list(lobj), '[1, 2.4, "qwer", "34", -456, true, null, false]'


def test_encode_dict(encoder):
    dobj = {"1": 2, 3: "4", True: "hhe", "ww": None, False: [1, -2]}
    assert encoder.encode_dict(dobj), '{"1": 2, 3: "4", true: "hhe", "ww": null, false: [1, -2]}'


class Custom(object):
    def hahaha(self):
        return 'hahahaha'


class MyEncoder(JSONEncoder):
    def __init__(self, *args, **kwargs):
        super(self.__class__, self).__init__(*args, **kwargs)

    def encode_Custom(self, obj):
        return '"{0}"'.format(obj.hahaha())


def test_encode_custom_obj():
    dobj = {"1": Custom(), 3: "4", True: "hhe", "ww": None, False: [1, -2]}
    encoder = MyEncoder(dobj)
    assert encoder.encode() == '{"1": "hahahaha", true: "hhe", 3: "4", "ww": null, false: [1, -2]}'
