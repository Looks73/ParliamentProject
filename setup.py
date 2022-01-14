#! /usr/bin/env python3
# coding: utf-8

from setuptools import setup
from setuptools import find_packages

# list dependencies from file
with open('requirements.txt') as f:
    content = f.readlines()
requirements = [x.strip() for x in content]

setup(name='analysis',
      description="analyse de fichiers",
      packages=find_packages(),
      install_requires=requirements)