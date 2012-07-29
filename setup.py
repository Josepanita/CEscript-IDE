import os
from setuptools import setup

# Utility function to read the README file.
# Used for the long_description.  It's nice, because now 1) we have a top level
# README file and 2) it's easier to type in the README file than to put a raw
# string in below ...
def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

setup(
    name = "cescript-ide",
    version = "0.1",
    author = "Jose Gomez",
    author_email = "jdgrodriguez@gmail.com",
    description = ("Lenguage C interpretado y en espanol para la introduccion a la programacion."),
    license = "BSD",
    keywords = "example documentation tutorial",
    url = "http://packages.python.org/cescript-ide",
    packages=['cescript-ide', 'tests'],
    long_description=read('README'),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Topic :: Utilities",
        "Intended Audience :: Education",
        "Natural Language :: Spanish", 
        "Programming Language :: Python",
        "Environment :: X11 Applications :: GTK",
        "License :: OSI Approved :: BSD License",
    ],
)