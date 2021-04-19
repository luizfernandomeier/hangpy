from os import path
from setuptools import setup, find_packages

this_directory = path.abspath(path.dirname(__file__))
with open(path.join(this_directory, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='hangpy',
    version='0.1.8',
    description="HangPy is a simple background job manager for Python",
    long_description=long_description,
    long_description_content_type='text/markdown',
    license='MIT',
    url="https://github.com/luizfernandomeier/hangpy",
    author='Luiz Fernando Meier',
    author_email='luizfernandomeier@gmail.com',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Programming Language :: Python :: 3.9'
    ],
    python_requires='>=3.9',
    install_requires=[
        'jsonpickle>=2.0.0',
        'redis>=3.5.3'
    ],
    packages=find_packages(),
    )
