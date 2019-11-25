#!/usr/bin/env python
# -*- encoding: utf-8 -*-
import io
from setuptools import setup


setup(name='merge_args',
      version='0.1.2',
      description='Merge signatures of two functions with Advanced Hackery.',
      keywords='merge_args',
      author='Chris Warrick',
      author_email='chris@chriswarrick.com',
      url='https://github.com/Kwpolska/merge_args',
      license='3-clause BSD',
      long_description=io.open(
          './README.rst', 'r', encoding='utf-8').read(),
      platforms='any',
      zip_safe=False,
      # http://pypi.python.org/pypi?%3Aaction=list_classifiers
      classifiers=['Development Status :: 1 - Planning',
                   'Programming Language :: Python',
                   'Programming Language :: Python :: 3',
                   'Programming Language :: Python :: 3.5',
                   'Programming Language :: Python :: 3.6',
                   'Programming Language :: Python :: 3.7',
                   'Programming Language :: Python :: 3.8',
                   ],
      py_modules=['merge_args'],
      )
