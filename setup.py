import os, sys, glob
from setuptools import setup
from glob import glob

def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

setup(
    name="metric_client",
    version="0.0.1",
    author="Mike Nilson",
    author_email="mike@blacksadhorse.com",
    description="UDP metric client pusher",
    license="BSD",
    keywords="metrica",
    url="http://blacksadhorse.com",
    packages=['metric_client'],
    install_requires=[
        'zerorpc'
    ],
    include_package_data=True,
    long_description=read('README'),
    classifiers=[
        "Development Status :: 0 - Alpha",
        "Topic :: Utilities",
        "License :: OSI Approved :: BSD License",
    ],
)
