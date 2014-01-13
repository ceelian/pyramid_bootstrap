#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys


try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

if sys.argv[-1] == 'publish':
    os.system('python setup.py sdist upload')
    sys.exit()

readme = open('README.rst').read()
history = open('CHANGELOG.rst').read().replace('.. :changelog:', '')

setup(
    name='pyramid_bootstrap',
    version='0.1.0',
    description='Bootstrap integration with Pyramid',
    long_description=readme + '\n\n' + history,
    author='Keith Yang',
    author_email='yang@keitheis.org',
    url='https://github.com/keitheis/pyramid_bootstrap',
    packages=[
        'pyramid_bootstrap',
    ],
    package_dir={'pyramid_bootstrap': 'pyramid_bootstrap'},
    include_package_data=True,
    install_requires=[
        "Pyramid>=1.3"
        "six>=1.5.2"
    ],
    license="BSD",
    zip_safe=False,
    keywords='pyramid_bootstrap',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Natural Language :: English',
        "Programming Language :: Python :: 2",
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
    ],
    test_suite='tests',
)
