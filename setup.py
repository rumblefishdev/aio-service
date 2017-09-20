import codecs

from os import path
from setuptools import setup, find_packages

__version__ = '0.0.1'

BASE_DIR = path.abspath(path.dirname(__file__))


def load_require(name):
    with open(path.join(BASE_DIR, 'requirements', name)) as p:
        return list(
            filter(len, [l.strip() for l in p])
        )


with codecs.open(path.join(BASE_DIR, 'README.md'), encoding='utf-8') as f:
    LONG_DESCRIPTION = f.read()

setup(
    name='aio-service',
    version=__version__,
    description='AIO service',
    long_description=LONG_DESCRIPTION,
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'Programming Language :: Python :: 3.6',
    ],
    packages=find_packages(exclude=['docs', 'tests*']),
    include_package_data=True,
    author='Mateusz Probachta',
    dependency_links=[],
    author_email='mateusz.probachta@pragmaticcoders.com',
    install_requires=load_require('default.txt'),
    extras_require={
        'redis': load_require('redis.txt'),
        'peewee': load_require('peewee.txt'),
        'queues': load_require('redis.txt')  # because queues are
    },
    setup_requires=[
        'pytest-runner==2.9'
    ],
    tests_require=load_require('test.txt')
)
