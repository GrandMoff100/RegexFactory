from setuptools import setup
from regexfactory import (
    __name__,
    __description__,
    __version__,
    __author__,
    __author_email__
)


setup(
    name=__name__,
    version=__version__,
    description=__description__,
    author=__author__,
    author_email=__author_email__,
    packages=["regexfactory"],
    long_description=open("README.md", "r").read(),
    long_description_content_type="text/markdown"
)
