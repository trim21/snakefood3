#!/usr/bin/env python
"""
Install script for the snakefood dependency graph tool.
"""
from setuptools import setup, find_packages

from snakefood3 import __version__

setup(
    name="snakefood3",
    version=__version__,
    description="Dependency Graphing for Python",
    long_description="",
    install_requires=['jinja2'],
    license="GPL",
    author="Trim21",
    author_email="trim21me@gmail.com",
    url="https://github.com/Trim21/snakefood3",
    packages=find_packages(),
)
