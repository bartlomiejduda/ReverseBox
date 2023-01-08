"""
Copyright © 2023  Bartłomiej Duda
License: GPL-3.0 License
"""

import pytest

from reversebox.hash.hash_sha2 import SHA2Handler
from tests.common import HashTestEntry

sha2_handler = SHA2Handler()


@pytest.mark.unittest
def test_hash_sha2_256_to_match_expected_result():
    sha2_data_list = [
        HashTestEntry(
            test_data=b"123",
            expected_result=b"\xa6\x65\xa4\x59\x20\x42\x2f\x9d\x41\x7e\x48\x67\xef\xdc\x4f\xb8\xa0\x4a\x1f\x3f\xff\x1f"
            b"\xa0\x7e\x99\x8e\x86\xf7\xf7\xa2\x7a\xe3",
        ),
        HashTestEntry(
            test_data=b"abcd",
            expected_result=b"\x88\xd4\x26\x6f\xd4\xe6\x33\x8d\x13\xb8\x45\xfc\xf2\x89\x57\x9d\x20\x9c\x89\x78\x23\xb9"
            b"\x21\x7d\xa3\xe1\x61\x93\x6f\x03\x15\x89",
        ),
        HashTestEntry(
            test_data=b"Secret123@456",
            expected_result=b"\xc9\xb6\x46\xb7\xd1\xa7\x67\x37\xed\x40\x97\x8e\x35\x10\x8d\xd4\x6e\xde\xb2\x0c\x81\x67"
            b"\x3f\x18\xa8\xda\x54\x7b\x01\x5c\xb0\x29",
        ),
        HashTestEntry(
            test_data=b"",
            expected_result=b"\xe3\xb0\xc4\x42\x98\xfc\x1c\x14\x9a\xfb\xf4\xc8\x99\x6f\xb9\x24\x27\xae\x41\xe4\x64\x9b"
            b"\x93\x4c\xa4\x95\x99\x1b\x78\x52\xb8\x55",
        ),
    ]

    for sha2_entry in sha2_data_list:
        test_result = sha2_handler.calculate_sha2_256_hash(sha2_entry.test_data)
        assert test_result == sha2_entry.expected_result
