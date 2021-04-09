from setuptools import setup, find_packages

setup(
    name='hangpy',
    version='0.1.3',
    install_requires=[
        'jsonpickle>=2.0.0',
        'redis>=3.5.3'
    ],
    packages=find_packages())
