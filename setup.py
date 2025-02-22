"""
Copyright © 2024-2025  Bartłomiej Duda
License: GPL-3.0 License
"""

import os
from typing import Final

import setuptools

VERSION_NUM: Final[str] = "0.25.5"


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
    keywords="ReverseBox, reverse engineering, RE, CRC, Hash, Encryption, Compression, Checksum, Python, image, decode, decoding, "
    "RGB, swizzle, swizzling, morton, twiddle, twiddling, texture, UYVY, YUY2, NV21, NV12, RGBA, RGBA8888, RGB565, RGBA8, BGR, "
    "grayscale, graphics, color, pixel, convert, converting, YUV, RAW, PSP, PS1, PS2, PS3, PS4, XBOX, X360, gamecube, dreamcast, "
    "BC, BC1, BC2, BC3, BC4, BC5, BC6, BC7, DXT1, DXT2, DXT3, PackBits, RLE, Macintosh, Jenkins, murmur, murmur3, one-at-a-time, "
    "additive",
    python_requires=">=3.6",
    install_requires=[
        "lzokay",
        "polib",
        "crc",
        "hashbase",
        "pillow",
        "mmh3",
    ],
    packages=setuptools.find_packages(exclude=["tests", "tests.*"]),
    package_data={"": ["libs/*.dll"]},
    include_package_data=True,
)
