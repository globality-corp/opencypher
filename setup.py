#!/usr/bin/env python
from setuptools import find_packages, setup

project = "opencypher"
version = "0.1.0"

setup(
    name=project,
    version=version,
    description="OpenCypher AST and Builder API",
    author="Globality Engineering",
    author_email="engineering@globality.com",
    url="https://github.com/globality-corp/opencypher",
    packages=find_packages(exclude=["*.tests", "*.tests.*", "tests.*", "tests"]),
    include_package_data=True,
    zip_safe=False,
    python_requires=">=3.7",
    keywords="opencypher cypher",
    install_requires=[
    ],
    setup_requires=[
        "nose>=1.3.7",
    ],
    dependency_links=[
    ],
    entry_points={
    },
    extras_require=dict(
        test="parameterized>=0.6.1",
    ),
    tests_require=[
        "coverage>=4.5.2",
        "parameterized>=0.6.1",
        "PyHamcrest>=1.9.0",
    ],
)
