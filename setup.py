#!/usr/bin/env python
from setuptools import setup, find_packages


setup(
    name = 'crew.metrics.backend',
    version = '0.1',
    packages = find_packages(),
    author = 'Crew',
    author_email = 'crew@ccs.neu.edu',
    description = 'Crew Metrics Backend',
    keywords = 'crew',
    entry_points = {
        'console_scripts': [
            'flamongo = crew.flamongo.main:main',
        ],
    },
    install_requires = [
        'pymongo >= 1.9',
        'Twisted >= 10.1',
        'pyopenssl',
    ],
)
