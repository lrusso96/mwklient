#!/usr/bin/env python
# encoding=utf-8
from __future__ import print_function
import os
import sys
from setuptools import setup

here = os.path.abspath(os.path.dirname(__file__))
README = open(os.path.join(here, 'README.md')).read()

needs_pytest = set(['pytest', 'test', 'ptr']).intersection(sys.argv)
pytest_runner = ['pytest-runner'] if needs_pytest else []

setup(name='mwklient',
      version='0.0.1',  # Use bumpversion to update
      description='MediaWiki API client',
      long_description=README,
      long_description_content_type='text/markdown',
      classifiers=[
          'Programming Language :: Python',
          'Programming Language :: Python :: 3.5',
          'Programming Language :: Python :: 3.6',
          'Programming Language :: Python :: 3.7',
      ],
      keywords='mediawiki wikipedia',
      author='Luigi Russo',
      author_email='russo.1699981@studenti.unroma1.it',
      url='https://github.com/lrusso96/mwklient',
      license='MIT',
      packages=['mwklient'],
      install_requires=['requests_oauthlib', 'six'],
      setup_requires=pytest_runner,
      tests_require=['pytest', 'pytest-pep8', 'pytest-cache', 'pytest-cov',
                     'responses>=0.3.0', 'responses!=0.6.0', 'mock'],
      zip_safe=True
      )
