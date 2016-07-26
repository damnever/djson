# -*- coding: utf-8 -*-

from __future__ import absolute_import
import sys

from .excs import JSONEncodeError


class Encoder(object):

    def __init__(self, obj):
        self._obj = obj

    def encode(self):
        return self._get_method(self._obj)()

    def _get_method(self, obj):
        type_name = type(obj)
        method = getattr(self, 'encode_' + type_name.__name__, None)
        if method is None:
            raise JSONEncodeError('Unsupported object: "{0}(type:{1})"'.format(
                obj, type_name))
        return (lambda: method(obj))

    def encode_dict(self, val_dict):
        items = list()
        get_method = self._get_method
        for k, v in val_dict.items():
            items.append('{0}: {1}'.format(get_method(k)(), get_method(v)()))
        return '{' + ','.join(items) + '}'

    def encode_list(self, val_ls):
        items = list()
        get_method = self._get_method
        for item in val_ls:
            items.append(get_method(item)())
        return '[' + ','.join(items) + ']'


    def encode_str(self, val_s):
        return '"{0}"'.format(val_s)

    def encode_bool(self, val_b, _bm={True: 'true', False: 'false'}):
        return _bm[val_b]

    def encode_int(self, val_num):
        return str(val_num)

    encode_float = encode_int

    def encode_NoneType(self, val_none):
        return "null"


def dump(obj, fd=sys.stdout, encoder=Encoder):
    fd.write(encoder(obj).encode())


def dumps(obj, encoder=Encoder):
    return encoder(obj).encode()