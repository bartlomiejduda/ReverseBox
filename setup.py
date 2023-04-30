"""
Copyright © 2023  Bartłomiej Duda
License: GPL-3.0 License
"""

import os

import setuptools

VERSION_NUM = "0.5.6"


def get_long_description() -> str:
    with open(
        os.path.join(os.path.dirname(__file__), "README.md"), encoding="utf8"
    ) as readme:
        readme_text = readme.read()
        return readme_text


setuptools.setup(
    name="ReverseBox",
    version=VERSION_NUM,
    author="Bartlomiej Duda",
    author_email="ikskoks@gmail.com",
    description="A set of functions useful in reverse engineering.",
    long_description=get_long_description(),
    long_description_content_type="text/markdown",
    url="https://github.com/bartlomiejduda/ReverseBox",
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Development Status :: 4 - Beta",
        "Topic :: Software Development",
        "Topic :: System :: Archiving :: Compression",
        "Topic :: Security :: Cryptography",
        "Environment :: Console",
        "Intended Audience :: Developers",
        "Intended Audience :: Science/Research",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Operating System :: OS Independent",
        "Natural Language :: English",
    ],
    test_suite="tests",
    keywords="ReverseBox, reverse engineering, RE, CRC, Hash, Encryption, Compression, Checksum, Python",
    python_requires=">=3.6",
    install_requires=["lzokay", "polib"],
    packages=setuptools.find_packages(),
)
