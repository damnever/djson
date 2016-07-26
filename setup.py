# -*- coding: utf-8 -*-

import re
import codecs

from setuptools import setup, find_packages

version = ''
with open('djson/__init__.py', 'r') as f:
        version = re.search(r'__version__\s*=\s*[\'"]([^\'"]*)[\'"]',
                            f.read(), re.M).group(1)

with codecs.open('README.rst', encoding='utf-8') as f:
    long_description = f.read()


setup(
    name='djson',
    version=version,
    description='A different JSON parser for Python.',
    long_description=long_description,
    author='Damnever',
    url='https://github.com/Damnever/djson',
    author_email='dxc.wolf@gmail.com',
    license='The BSD 3-Clause License',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'Topic :: Utilities',
        'License :: OSI Approved :: BSD License',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 3',
    ],
    keywords='djson, good, json',
    packages=find_packages(),
)
