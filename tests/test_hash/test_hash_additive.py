"""
Copyright © 2025  Bartłomiej Duda
License: GPL-3.0 License
"""

import pytest

from reversebox.common.common import convert_int_to_hex_string
from reversebox.hash.hash_additive import AdditiveHashHandler
from tests.common import BytesHashTestEntry, TextHashTestEntry

additive_hash_handler = AdditiveHashHandler()


# fmt: off

@pytest.mark.unittest
def test_hash_additive_from_string_to_match_expected_result():
    hash_data_list = [
        TextHashTestEntry(test_string="test", expected_int=452, expected_str="0x1C4", prime=222333),
        TextHashTestEntry(test_string="Hello World!", expected_int=1097, expected_str="0x449", prime=222333),
    ]

    for hash_entry in hash_data_list:
        # check expected result from first execution
        test_result = additive_hash_handler.calculate_additive_hash_from_string(hash_entry.test_string, hash_entry.prime)
        test_result_str = convert_int_to_hex_string(test_result)
        assert test_result == hash_entry.expected_int
        assert test_result_str == hash_entry.expected_str

        # check if result is the same after second execution
        test_result = additive_hash_handler.calculate_additive_hash_from_string(hash_entry.test_string, hash_entry.prime)
        test_result_str = convert_int_to_hex_string(test_result)
        assert test_result == hash_entry.expected_int
        assert test_result_str == hash_entry.expected_str


@pytest.mark.unittest
def test_hash_additive_from_bytes_to_match_expected_result():
    hash_data_list = [
        BytesHashTestEntry(test_bytes=b"test", expected_int=452, expected_str="0x1C4", prime=222333),
        BytesHashTestEntry(test_bytes=b"Hello World!", expected_int=1097, expected_str="0x449", prime=222333),
    ]

    for hash_entry in hash_data_list:
        # check expected result from first execution
        test_result = additive_hash_handler.calculate_additive_hash_from_bytes(hash_entry.test_bytes, hash_entry.prime)
        test_result_str = convert_int_to_hex_string(test_result)
        assert test_result == hash_entry.expected_int
        assert test_result_str == hash_entry.expected_str

        # check if result is the same after second execution
        test_result = additive_hash_handler.calculate_additive_hash_from_bytes(hash_entry.test_bytes, hash_entry.prime)
        test_result_str = convert_int_to_hex_string(test_result)
        assert test_result == hash_entry.expected_int
        assert test_result_str == hash_entry.expected_str
