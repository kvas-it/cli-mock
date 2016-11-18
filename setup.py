"""Install cli_mock module."""

from setuptools import setup

from io import open
from os import path

here = path.abspath(path.dirname(__file__))

with open(path.join(here, 'README.rst'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='cli_mock',
    version='0.2.0',
    description='Mock command line utils by replaying recorded invocations',
    long_description=long_description,
    url='https://github.com/kvas-it/cli-mock',
    author='Vasily Kuznetsov',
    author_email='kvas.it@gmail.com',
    license='MIT',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Testing',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
    ],
    keywords='cli console mock record replay',
    packages=['cli_mock'],
    install_requires=[],
    entry_points={
        'console_scripts': [
            'crecord=cli_mock.crecord:main',
            'creplay=cli_mock.creplay:main',
        ],
        'pytest11': [
            'cli-mock = cli_mock.pytest_plugin',
        ],
    },
)
