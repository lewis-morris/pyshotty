from setuptools import setup

from os import path

this_directory = path.abspath(path.dirname(__file__))
with open(path.join(this_directory, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='pyshotty',
    version='0.0.3.5',
    packages=['pyshotty'],
    url='https://github.com/lewis-morris/pyshotty',
    license='MIT',
    author='Lewis Morris',
    author_email='lewism@codeus.co.uk',
    description='Python website screen grabber',
    long_description = long_description,
    long_description_content_type = 'text/markdown'
)
