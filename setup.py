"""
Copyright © 2022  Bartłomiej Duda
License: GPL-3.0 License
"""

import os
import setuptools

VERSION_NUM = "0.0.1"


def get_long_description() -> str:
    with open(os.path.join(os.path.dirname(__file__), "README.md")) as readme:
        readme_text = readme.read()
        return readme_text


setuptools.setup(
    name="ReverseBox",
    version=VERSION_NUM,
    author="Bartlomiej Duda",
    author_email="ikskoks@gmail.com",
    license="GPL-3.0",
    description="A set of functions useful in reverse engineering.",
    long_description=get_long_description(),
    long_description_content_type="text/markdown",
    url="https://github.com/bartlomiejduda/ReverseBox",
    classifiers=[
        "Programming Language :: Python :: 3",
        "Environment :: Console",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: GPL-3.0 License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
    install_requires=[],
)