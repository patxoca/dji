# -*- coding: utf-8 -*-

# $Id:$

import codecs
import os

from setuptools import setup, find_packages


version = "0.1.0"


def read(*path_components):
    with codecs.open(os.path.join(*path_components), "r") as f:
        return f.read()


setup(
    name="djira",
    version=version,
    description="Django Introspection REST API.",
    long_description=read("README.rst"),
    classifiers=[
        "Development Status :: 1 - Planning",
        "Environment :: Web Environment",
        "Framework :: Django",
        "Framework :: Django :: 1.9",
        "Framework :: Django :: 1.10",
        "Framework :: Django :: 1.11",
        "Framework :: Django :: 2.0",
        "Framework :: Django :: 2.1",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)",
        "Natural Language :: English",
        "Operating System :: POSIX :: Linux",
        "Programming Language :: Python",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3.4",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: Implementation :: CPython",
        "Topic :: Software Development",
    ],
    keywords="",
    author="Alexis Roda",
    author_email="alexis.roda.villalonga@gmail.com",
    url="https://github.com/patxoca/djira",
    license="GPL",
    packages=find_packages(exclude=["ez_setup"]),
    namespace_packages=[],
    include_package_data=True,
    zip_safe=False,
    install_requires=[
        "setuptools",
        "django",
        "pluggy",
    ],
    entry_points={
    },
)
