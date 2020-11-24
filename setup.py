# !/usr/bin/env python
# -*- coding: utf-8 -*-
"""Find out more at REPO_URL."""
import codecs
import os
import re
from setuptools.command.test import test as TestCommand
from setuptools import find_packages
from setuptools import setup
import sys


ROOT_DIR = os.path.abspath(os.path.dirname(__file__))
os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir)))


INSTALL_REQUIREMENTS = [
    # A string or list of strings specifying what other distributions need to
    # be installed when this one is.
    "git+git://github.com/AUSSDA/pyDataverse.git@3b040ff23b665ec2650bebcf4bd5478de6881af0",
    "pytest==6.1.2",
    "selenium==3.141.0",
    "requests==2.25.0",
    "pydantic==1.7.2",
]

SETUP_REQUIREMENTS = []

TESTS_REQUIREMENTS = []

# TESTS_REQUIREMENTS =read_file("requirements/test.txt")

CLASSIFIERS = [
    # How mature is this project? Common values are
    #   2 - Pre-Alpha
    #   3 - Alpha
    #   4 - Beta
    #   5 - Production/Stable
    "Development Status :: 3 - Alpha",
    "Intended Audience :: Developers",
    "Operating System :: OS Independent",
    "License :: OSI Approved :: MIT License",
    "Programming Language :: Python",
    "Programming Language :: Python :: 3.6",
    "Programming Language :: Python :: 3.7",
    "Programming Language :: Python :: 3.8",
    "Natural Language :: English",
]

setup(
    author="Stefan Kasberger",
    author_email="stefan.kasberger@univie.ac.at",
    name="AUSSDA Tests",
    description="Selenium tests for AUSSDA",
    long_description=read_file("README.md"),
    long_description_content_type="text/markdown",
    license="MIT",
    url="https://github.com/AUSSDA/aussda_tests",
    python_requires=">=3.6",
    platforms=["OS Independent"],
    classifiers=CLASSIFIERS,
    install_requires=INSTALL_REQUIREMENTS,
    packages=find_packages(),
    setup_requires=SETUP_REQUIREMENTS,
    tests_require=TESTS_REQUIREMENTS,
    include_package_data=True,
    keywords=[""],
    zip_safe=False,
    project_urls={"Issue Tracker": "https://github.com/AUSSDA/aussda_tests/issues",},
)
