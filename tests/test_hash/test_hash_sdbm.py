"""
Copyright © 2024  Bartłomiej Duda
License: GPL-3.0 License
"""

import pytest

from reversebox.common.common import convert_int_to_hex_string
from reversebox.hash.hash_sdbm import SDBMHandler
from tests.common import BytesHashTestEntry, TextHashTestEntry

sdbm_handler = SDBMHandler()


# fmt: off

@pytest.mark.unittest
def test_hash_sdbm_from_string_to_match_expected_result():
    hash_data_list = [
        # TextHashTestEntry(
        TextHashTestEntry(test_string="Hello", expected_int=2873473298, expected_str="0xAB45B912"),
        TextHashTestEntry(test_string="Hello!", expected_int=3745155983, expected_str="0xDF3A8B8F"),
        TextHashTestEntry(test_string="abcd", expected_int=3518636162, expected_str="0xD1BA2082"),
        TextHashTestEntry(test_string="123456789", expected_int=1755344949, expected_str="0x68A07035"),
        TextHashTestEntry(test_string="123", expected_int=408093746, expected_str="0x18530432"),
        TextHashTestEntry(test_string="Secret123@123", expected_int=3823733940, expected_str="0xE3E98CB4"),
        TextHashTestEntry(test_string="", expected_int=0, expected_str="0x00"),
        TextHashTestEntry(test_string=" ", expected_int=32, expected_str="0x20"),
    ]

    for hash_entry in hash_data_list:
        # check expected result from first execution
        test_result = sdbm_handler.calculate_sdbm_hash_from_string(hash_entry.test_string)
        test_result_str = convert_int_to_hex_string(test_result)
        assert test_result == hash_entry.expected_int
        assert test_result_str == hash_entry.expected_str

        # check if result is the same after second execution
        test_result = sdbm_handler.calculate_sdbm_hash_from_string(hash_entry.test_string)
        test_result_str = convert_int_to_hex_string(test_result)
        assert test_result == hash_entry.expected_int
        assert test_result_str == hash_entry.expected_str


@pytest.mark.unittest
def test_hash_sdbm_from_bytes_to_match_expected_result():
    hash_data_list = [
        BytesHashTestEntry(test_bytes=b"Hello", expected_int=2873473298, expected_str="0xAB45B912"),
        BytesHashTestEntry(test_bytes=b"Hello!", expected_int=3745155983, expected_str="0xDF3A8B8F"),
        BytesHashTestEntry(test_bytes=b"abcd", expected_int=3518636162, expected_str="0xD1BA2082"),
        BytesHashTestEntry(test_bytes=b"123456789", expected_int=1755344949, expected_str="0x68A07035"),
        BytesHashTestEntry(test_bytes=b"123", expected_int=408093746, expected_str="0x18530432"),
        BytesHashTestEntry(test_bytes=b"Secret123@123", expected_int=3823733940, expected_str="0xE3E98CB4"),
        BytesHashTestEntry(test_bytes=b"", expected_int=0, expected_str="0x00"),
        BytesHashTestEntry(test_bytes=b" ", expected_int=32, expected_str="0x20"),
    ]

    for hash_entry in hash_data_list:
        # check expected result from first execution
        test_result = sdbm_handler.calculate_sdbm_hash_from_bytes(hash_entry.test_bytes)
        test_result_str = convert_int_to_hex_string(test_result)
        assert test_result == hash_entry.expected_int
        assert test_result_str == hash_entry.expected_str

        # check if result is the same after second execution
        test_result = sdbm_handler.calculate_sdbm_hash_from_bytes(hash_entry.test_bytes)
        test_result_str = convert_int_to_hex_string(test_result)
        assert test_result == hash_entry.expected_int
        assert test_result_str == hash_entry.expected_str


# fmt: on
