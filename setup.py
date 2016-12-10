#!/usr/bin/env python

from os.path import exists
from setuptools import setup, find_packages


setup(
    name='seed',
    version=open('VERSION').read().strip(),
    author='Adam Charnock',
    author_email='adam@adamcharnock.com',
    packages=find_packages(),
    scripts=[],
    url='https://github.com/adamcharnock/seed',
    license='MIT',
    description='A utility for easily creating and releasing Python packages',
    long_description=open('README.rst').read() if exists("README.rst") else "",
    entry_points=dict(console_scripts=['seed=seed.run:main']),
    install_requires=[
        "path.py>=2.2.2",
        'wheel',
    ],
    classifiers=[
        'Environment :: Console',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Topic :: System :: Software Distribution',
    ],
)
