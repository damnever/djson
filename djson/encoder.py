# -*- coding: utf-8 -*-

from __future__ import absolute_import
import sys

from .exc import JSONEncodeError
from .utils import to_utf8


class JSONEncoder(object):

    def __init__(self, obj):
        self._obj = obj

    def encode(self):
        return to_utf8(self._get_method(self._obj)())

    def _get_method(self, obj):
        type_name = type(obj)
        method = getattr(self, 'encode_' + type_name.__name__, None)
        if method is None:
            raise JSONEncodeError('unsupported object: "{0}(type:{1})"'.format(
                obj, type_name))
        return (lambda: method(obj))

    def encode_dict(self, val_dict):
        items = list()
        get_method = self._get_method
        for k, v in val_dict.items():
            items.append('{0}: {1}'.format(get_method(k)(), get_method(v)()))
        return '{' + ', '.join(items) + '}'

    def encode_list(self, val_ls):
        items = list()
        get_method = self._get_method
        for item in val_ls:
            items.append(get_method(item)())
        return '[' + ', '.join(items) + ']'

    def encode_bool(self, val_b, _bm={True: 'true', False: 'false'}):
        return _bm[val_b]

    def encode_int(self, val_num):
        return '{0}'.format(val_num)

    encode_float = encode_int

    def encode_NoneType(self, val_none):
        return "null"

    def encode_str(self, val_s):
        return '"{0}"'.format(val_s)

    encode_unicode = encode_str  # Py2
    encode_bytes = encode_str  # Py3



def dump(obj, file=sys.stdout, encoder=JSONEncoder):
    file.write(encoder(obj).encode())
    if hasattr(file, 'flush'):
        file.flush()


def dumps(obj, encoder=JSONEncoder):
    return encoder(obj).encode()
