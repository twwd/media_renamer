from setuptools import setup, find_packages


with open('README.rst') as f:
    readme = f.read()

with open('LICENSE') as f:
    license = f.read()

setup(
    name='media_renamer',
    version='0.0.1',
    description='Script for renaming media files as their creation date',
    long_description=readme,
    author='Tim Walter',
    author_email='tim@twwd.de',
    url='TODO',
    license=license,
    packages=find_packages(exclude=('tests', 'docs'))
)

