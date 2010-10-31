#!/usr/bin/env python
from distutils.core import setup


setup(
    name = 'crew.flamongo',
    version = '0.1',
    packages = ['crew', 'crew.flamongo'],
    author = 'Crew',
    author_email = 'crew@ccs.neu.edu',
    description = 'Crew Flamongo',
    keywords = 'crew',
    scripts = ['scripts/flamongo'],
)
