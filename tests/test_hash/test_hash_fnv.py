"""
Copyright © 2023  Bartłomiej Duda
License: GPL-3.0 License
"""

import pytest

from reversebox.hash.hash_fnv import FNVHashHandler
from tests.common import HashTestEntry

fnv_handler = FNVHashHandler()


@pytest.mark.unittest
def test_hash_fnv1_32_to_match_expected_result():
    fnv_data_list = [
        HashTestEntry(
            test_data=b"123",
            expected_result=b"\xbb\x07\xd6\x72",
        ),
        HashTestEntry(
            test_data=b"abcd",
            expected_result=b"\x75\x73\xDE\xB9",
        ),
        HashTestEntry(
            test_data=b"Secret123@456",
            expected_result=b"\xFE\xE7\xFF\x9F",
        ),
        HashTestEntry(
            test_data=b"",
            expected_result=b"\xc5\x9d\x1c\x81",
        ),
    ]

    for fnv_entry in fnv_data_list:
        test_result = fnv_handler.fnv1_32(fnv_entry.test_data)
        assert test_result == fnv_entry.expected_result


@pytest.mark.unittest
def test_hash_fnv1a_32_to_match_expected_result():
    fnv_data_list = [
        HashTestEntry(
            test_data=b"123",
            expected_result=b"\x1B\x63\x38\x72",
        ),
        HashTestEntry(
            test_data=b"abcd",
            expected_result=b"\xBD\x79\x34\xCE",
        ),
        # TODO - check out why those results are different than in "WinHash" tool
        # HashTestEntry(
        #     test_data=b"Secret123@456",
        #     expected_result=b"\x74\xB4\x3B\x49",
        # ),
        # HashTestEntry(
        #     test_data=b"",
        #     expected_result=b"\x00\x00\x00\x00",
        # ),
    ]

    for fnv_entry in fnv_data_list:
        test_result = fnv_handler.fnv1a_32(fnv_entry.test_data)
        assert test_result == fnv_entry.expected_result
