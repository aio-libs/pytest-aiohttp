import codecs
import os
import re
import sys
from setuptools import setup


with codecs.open(os.path.join(os.path.abspath(os.path.dirname(
        __file__)), 'pytest_aiohttp', '__init__.py'), 'r', 'latin1') as fp:
    try:
        version = re.findall(r"^__version__ = '([^']+)'\r?$",
                             fp.read(), re.M)[0]
    except IndexError:
        raise RuntimeError('Unable to determine version.')


def read(f):
    return open(os.path.join(os.path.dirname(__file__), f)).read().strip()


setup(
    name='pytest-aiohttp',
    version=version,
    description=('pytest plugin for aiohttp support'),
    long_description='\n\n'.join((read('README.rst'), read('CHANGES.rst'))),
    classifiers=[
        'License :: OSI Approved :: Apache Software License',
        'Intended Audience :: Developers',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Topic :: Software Development :: Testing',
        'Framework :: Pytest',
        'Framework :: AsyncIO',
    ],
    author='Andrew Svetlov',
    author_email='andrew.svetlov@gmail.com',
    url='https://github.com/aio-libs/pytest-aiohttp/',
    license='Apache 2',
    install_requires=[
        'pytest',
        'aiohttp>=0.22.0'
    ],
    packages=['pytest_aiohttp'],
    entry_points={
        'pytest11': ['aiohttp = pytest_aiohttp'],
    },
)
