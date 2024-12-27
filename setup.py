from distutils.core import setup
from setuptools import find_packages

setup(
    name = "flaskner",
    version = "0.0.1",
    description = "a simple NER API",
    packages=find_packages(include=['TddPytest', 'MyVenv', 'Static', 'templates', 'test'])
)