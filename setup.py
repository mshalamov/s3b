#!/usr/bin/env python
from setuptools import setup, find_packages

setup(
    name='s3b',
    version='0.0.1',
    author='Maksym Shalamov',
    author_email='mshalamov@mirantis.com',
    packages=find_packages(),
    entry_points={
        'console_scripts': [
            's3b = s3b.runner:main',
        ],
    },
)