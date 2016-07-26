# -*- coding: utf-8 -*-


from __future__ import absolute_import

from .decoder import loads, load
from .encoder import dumps, dump, Encoder
from .excs import JSONDecodeError, JSONEncodeError


version = __version__ = '0.1.0'
version_info = [int(num) for num in version.split('.')]
author = __author__ = 'Damnever <dxc.wolf@gmail.com>'

__all__ = ['loads', 'load', 'dumps', 'dump', 'Encoder',
           'JSONDecodeError', 'JSONEncodeError',
           '__version__', 'version', 'version_info',
           'author', '__author__']
