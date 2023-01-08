"""
Copyright © 2022  Bartłomiej Duda
License: GPL-3.0 License
"""

import pytest

from reversebox.hash.hash_md5 import MD5Handler
from tests.common import HashTestEntry

md5_handler = MD5Handler()


@pytest.mark.unittest
def test_hash_md5_to_match_expected_result():
    md5_data_list = [
        HashTestEntry(
            test_data=b"123",
            expected_result=b"\x20\x2C\xB9\x62\xAC\x59\x07\x5B\x96\x4B\x07\x15\x2D\x23\x4B\x70",
        ),
        HashTestEntry(
            test_data=b"abcd",
            expected_result=b"\xE2\xFC\x71\x4C\x47\x27\xEE\x93\x95\xF3\x24\xCD\x2E\x7F\x33\x1F",
        ),
        HashTestEntry(
            test_data=b"Secret123@456",
            expected_result=b"\x7A\xB9\xCE\x89\x8E\x1D\xB2\x18\x99\x44\xB3\xE6\x38\x3A\x58\x6E",
        ),
        HashTestEntry(
            test_data=b"",
            expected_result=b"\xD4\x1D\x8C\xD9\x8F\x00\xB2\x04\xE9\x80\x09\x98\xEC\xF8\x42\x7E",
        ),
    ]

    for md5_entry in md5_data_list:
        test_result = md5_handler.calculate_md5_hash(md5_entry.test_data)
        assert test_result == md5_entry.expected_result
