"""
Copyright © 2023  Bartłomiej Duda
License: GPL-3.0 License
"""

import pytest

from reversebox.hash.hash_md2 import MD2Handler
from tests.common import HashTestEntry

md2_handler = MD2Handler()


@pytest.mark.unittest
def test_hash_md2_to_match_expected_result():
    md2_data_list = [
        HashTestEntry(
            test_data=b"123",
            expected_result=b"\xef\x1f\xed\xf5\xd3\x2e\xad\x6b\x7a\xaf\x68\x7d\xe4\xed\x1b\x71",
        ),
        HashTestEntry(
            test_data=b"abcd",
            expected_result=b"\xf7\x90\xd2\xa3\x94\x0d\xde\x40\x56\x38\x7c\x78\x7f\x30\x62\xf8",
        ),
        HashTestEntry(
            test_data=b"Secret123@456",
            expected_result=b"\xf2\xc8\x23\xd8\xee\x44\x54\xf1\xc4\x20\xb3\x8a\x1c\x1c\xae\x67",
        ),
        HashTestEntry(
            test_data=b"",
            expected_result=b"\x83\x50\xe5\xa3\xe2\x4c\x15\x3d\xf2\x27\x5c\x9f\x80\x69\x27\x73",
        ),
    ]

    for md2_entry in md2_data_list:
        test_result = md2_handler.calculate_md2_hash(md2_entry.test_data)
        assert test_result == md2_entry.expected_result
