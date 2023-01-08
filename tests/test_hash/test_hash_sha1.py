"""
Copyright © 2023  Bartłomiej Duda
License: GPL-3.0 License
"""

import pytest

from reversebox.hash.hash_sha1 import SHA1Handler
from tests.common import HashTestEntry

sha1_handler = SHA1Handler()


@pytest.mark.unittest
def test_hash_sha1_to_match_expected_result():
    sha1_data_list = [
        HashTestEntry(
            test_data=b"123",
            expected_result=b"\x40\xbd\x00\x15\x63\x08\x5f\xc3\x51\x65\x32\x9e\xa1\xff\x5c\x5e\xcb\xdb\xbe\xef",
        ),
        HashTestEntry(
            test_data=b"abcd",
            expected_result=b"\x81\xfe\x8b\xfe\x87\x57\x6c\x3e\xcb\x22\x42\x6f\x8e\x57\x84\x73\x82\x91\x7a\xcf",
        ),
        HashTestEntry(
            test_data=b"Secret123@456",
            expected_result=b"\x95\x97\x91\x1b\x10\x41\x98\xf2\x96\x8c\xc1\xfe\xca\x2e\x6a\x3e\x06\x0c\x15\xb4",
        ),
        HashTestEntry(
            test_data=b"",
            expected_result=b"\xda\x39\xa3\xee\x5e\x6b\x4b\x0d\x32\x55\xbf\xef\x95\x60\x18\x90\xaf\xd8\x07\x09",
        ),
    ]

    for sha1_entry in sha1_data_list:
        test_result = sha1_handler.calculate_sha1_hash(sha1_entry.test_data)
        assert test_result == sha1_entry.expected_result
