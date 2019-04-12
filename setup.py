#!/usr/bin/env python
"""
Install script for the snakefood dependency graph tool.
"""
from setuptools import setup

from snakefood3 import __version__

setup(
    name="snakefood3",
    version=__version__,
    description="Dependency Graphing for Python",
    long_description="""
Generate dependencies from Python code, filter, cluster and generate graphs
from the dependency list.
""",
    license="GPL",
    author="Martin Blais",
    author_email="blais@furius.ca",
    url="http://furius.ca/snakefood",
    download_url="http://bitbucket.org/blais/snakefood",
    package_dir={'': 'lib/python'},
    packages=['snakefood', 'snakefood/fallback'],
    scripts=scripts
)
