# -*- coding: utf-8 -*-

from setuptools import setup, find_packages


with open('README.md') as f:
    readme = f.read()

with open('LICENSE') as f:
    license = f.read()

setup(
    name='sample',
    version='0.0.0',
    description='ToyLanguage-Python',
    long_description=readme,
    author='Ian J. Bertolacci',
    author_email='ian.bertolacci@gmail.com',
    url='https://github.com/ian-bertolacci/ToyLanguage-Python',
    license=license,
    packages=find_packages(exclude=('tests', 'docs'))
)
