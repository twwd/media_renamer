# -*- coding: utf-8 -*-
from setuptools import setup, find_packages

with open('README.md') as f:
    readme = f.read()

with open('LICENSE') as f:
    lic = f.read()

setup(
    name='media_renamer',
    version='0.0.1',
    description='A simple tool for renaming media files as their creation date',
    long_description=readme,
    author='Tim Walter',
    author_email='tim@twwd.de',
    url='https://github.com/twwd/media_renamer',
    license=lic,
    packages=find_packages(exclude=('tests', 'docs'))
)
