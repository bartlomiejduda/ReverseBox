"""
Copyright © 2022  Bartłomiej Duda
License: GPL-3.0 License
"""

from dataclasses import dataclass


@dataclass
class CRCTestEntry:
    test_data: bytes
    expected_int: int
    expected_str: str


@dataclass
class XORTestEntry:
    test_data: bytes
    key: bytes
    expected_result: bytes


@dataclass
class XORRetro64ECOTestEntry:
    test_data: bytes
    key: int
    expected_result: bytes


@dataclass
class MD5TestEntry:
    test_data: bytes
    expected_result: bytes
