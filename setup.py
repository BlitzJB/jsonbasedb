from setuptools import setup, find_packages

setup(
  name='jsonbasedb',
  version='1.0.1',
  author='BlitzJB',
  author_email='blitz04.dev@gmail.com',
  description='A simple library for interacting with jsonbase',
  long_description=open('README.md').read(),
  long_description_content_type='text/markdown',
  url='https://github.com/BlitzJB/jsonbasedb',
  packages=find_packages(),
  install_requires=['requests'],
  keywords=['python', 'json', 'database', 'jsonbase'],
  classifiers=[
    "Development Status :: 1 - Planning",
    "Intended Audience :: Developers",
    "Programming Language :: Python :: 3",
    "Operating System :: Unix",
    "Operating System :: MacOS :: MacOS X",
    "Operating System :: Microsoft :: Windows",
  ]
)