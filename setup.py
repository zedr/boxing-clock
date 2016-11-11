"""Boxing clock setup file.
"""

# Always prefer setuptools over distutils
from setuptools import setup, find_packages
# To use a consistent encoding
from codecs import open
from os import path

here = path.abspath(path.dirname(__file__))

# Get the long description from the README file
with open(path.join(here, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='boxe_clock',
    version='1.0.3',

    description='A simple boxing timer for mobile devices',
    long_description=long_description,

    url='',

    # Author details
    author='Rigel Di Scala',
    author_email='zedr@zedr.com',

    license='MIT',

    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Topic :: Other/Nonlisted Topic',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
    ],

    keywords='game',

    packages=find_packages("src"),
    package_dir={'': 'src'},

    install_requires=['kivy==1.9.1', 'cython', 'jnius'],
)
