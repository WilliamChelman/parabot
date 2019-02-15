#!/usr/bin/env python
# encoding: utf-8

from setuptools import setup, find_packages

import parabot

setup(
    name="parabot",
    version=parabot.__version__,
    packages=find_packages(),
    long_description=open('README.md').read(),
    include_package_data=True,
    entry_points={
        'console_scripts': [
            'parabot = parabot.wsgi:main',
        ],
    },
    zip_safe=False
)
