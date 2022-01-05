from setuptools import setup, find_packages

setup(
  name='jsonbasedb',
  version='1.2.1',
  author='BlitzJB',
  author_email='blitz04.dev@gmail.com',
  description='A simple library for interacting with jsonbase',
  long_description=open('README.md').read(),
  long_description_content_type='text/markdown',
  url='https://github.com/BlitzJB/jsonbasedb',
  packages=find_packages(),
  install_requires=['requests'],
  keywords=['python', 'json', 'database', 'jsonbase'],
)