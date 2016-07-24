# -*- coding: utf-8 -*-

from djson import dumps, JSONEncodeError, Encoder


json_obj = {
    'hahah': 12421,
    1231: 'fghdf',
    4.5: [None, 'f', 4, '6.5'],
    'ete': True,
    'iui': False,
}

class AA(object):
    pass

json_obj2 = {
    'custom': AA(),
}


class MyEncoder(Encoder):
    def __init__(self, *args, **kwargs):
        super(self.__class__, self).__init__(*args, **kwargs)

    def encode_AA(self, obj):
        return '"aa"'


if __name__ == '__main__':
    print(dumps(json_obj))

    print('--')
    try:
        print(dumps(json_obj2))
    except JSONEncodeError as e:
        print(e)

    print('--')
    print(dumps(json_obj2, encoder=MyEncoder))
