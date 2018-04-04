#!/usr/bin/env python3
# -*- coding: utf-8 -*-

'''
Setup script for ChirpText.

Latest version can be found at https://github.com/letuananh/chirptext

:copyright: (c) 2012 Le Tuan Anh <tuananh.ke@gmail.com>
:license: MIT, see LICENSE for more details.
'''

import io
import os
from setuptools import setup

import chirptext


def read(*filenames, **kwargs):
    encoding = kwargs.get('encoding', 'utf-8')
    sep = kwargs.get('sep', '\n')
    buf = []
    for filename in filenames:
        with io.open(filename, encoding=encoding) as f:
            buf.append(f.read())
    return sep.join(buf)


readme_file = 'README.rst' if os.path.isfile('README.rst') else 'README.md'
print("README file: {}".format(readme_file))
long_description = read(readme_file)

setup(
    name='chirptext',
    version=chirptext.__version__,
    url=chirptext.__url__,
    project_urls={
        "Bug Tracker": "https://github.com/letuananh/chirptext/issues",
        "Source Code": "https://github.com/letuananh/chirptext/"
    },
    keywords="nlp",
    license=chirptext.__license__,
    author=chirptext.__author__,
    tests_require=[],
    install_requires=[],
    author_email=chirptext.__email__,
    description=chirptext.__description__,
    long_description=long_description,
    packages=['chirptext'],
    package_data={'chirptext': ['data/luke/swadesh/*.txt',
                                'data/sino/*.csv']},
    include_package_data=True,
    platforms='any',
    test_suite='test',
    # Reference: https://pypi.python.org/pypi?%3Aaction=list_classifiers
    classifiers=['Programming Language :: Python',
                 'Development Status :: 2 - Pre-Alpha',
                 'Natural Language :: English',
                 'Environment :: Plugins',
                 'Intended Audience :: Developers',
                 'License :: OSI Approved :: {}'.format(chirptext.__license__),
                 'Operating System :: OS Independent',
                 'Topic :: Text Processing',
                 'Topic :: Software Development :: Libraries :: Python Modules']
)
