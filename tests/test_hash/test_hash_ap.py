"""
Copyright © 2024  Bartłomiej Duda
License: GPL-3.0 License
"""

import pytest

from reversebox.common.common import convert_int_to_hex_string
from reversebox.hash.hash_ap import APHandler
from tests.common import BytesHashTestEntry, TextHashTestEntry

ap_handler = APHandler()


# fmt: off

@pytest.mark.unittest
def test_hash_ap_from_string_to_match_expected_result():
    hash_data_list = [
        # TextHashTestEntry(
        TextHashTestEntry(test_string="Hello", expected_int=2231986490, expected_str="0x8509693A"),
        TextHashTestEntry(test_string="Hello!", expected_int=764874157, expected_str="0x2D970DAD"),
        TextHashTestEntry(test_string="abcd", expected_int=722761359, expected_str="0x2B14768F"),
        TextHashTestEntry(test_string="123456789", expected_int=2777544090, expected_str="0xA58DF59A"),
        TextHashTestEntry(test_string="123", expected_int=3978747199, expected_str="0xED26DD3F"),
        TextHashTestEntry(test_string="Secret123@123", expected_int=3048918585, expected_str="0xB5BACE39"),
        TextHashTestEntry(test_string="", expected_int=2863311530, expected_str="0xAAAAAAAA"),
        TextHashTestEntry(test_string=" ", expected_int=1431655690, expected_str="0x5555550A"),
    ]

    for hash_entry in hash_data_list:
        # check expected result from first execution
        test_result = ap_handler.calculate_ap_hash_from_string(hash_entry.test_string)
        test_result_str = convert_int_to_hex_string(test_result)
        assert test_result == hash_entry.expected_int
        assert test_result_str == hash_entry.expected_str

        # check if result is the same after second execution
        test_result = ap_handler.calculate_ap_hash_from_string(hash_entry.test_string)
        test_result_str = convert_int_to_hex_string(test_result)
        assert test_result == hash_entry.expected_int
        assert test_result_str == hash_entry.expected_str


@pytest.mark.unittest
def test_hash_ap_from_bytes_to_match_expected_result():
    hash_data_list = [
        BytesHashTestEntry(test_bytes=b"Hello", expected_int=2231986490, expected_str="0x8509693A"),
        BytesHashTestEntry(test_bytes=b"Hello!", expected_int=764874157, expected_str="0x2D970DAD"),
        BytesHashTestEntry(test_bytes=b"abcd", expected_int=722761359, expected_str="0x2B14768F"),
        BytesHashTestEntry(test_bytes=b"123456789", expected_int=2777544090, expected_str="0xA58DF59A"),
        BytesHashTestEntry(test_bytes=b"123", expected_int=3978747199, expected_str="0xED26DD3F"),
        BytesHashTestEntry(test_bytes=b"Secret123@123", expected_int=3048918585, expected_str="0xB5BACE39"),
        BytesHashTestEntry(test_bytes=b"", expected_int=2863311530, expected_str="0xAAAAAAAA"),
        BytesHashTestEntry(test_bytes=b" ", expected_int=1431655690, expected_str="0x5555550A"),
    ]

    for hash_entry in hash_data_list:
        # check expected result from first execution
        test_result = ap_handler.calculate_ap_hash_from_bytes(hash_entry.test_bytes)
        test_result_str = convert_int_to_hex_string(test_result)
        assert test_result == hash_entry.expected_int
        assert test_result_str == hash_entry.expected_str

        # check if result is the same after second execution
        test_result = ap_handler.calculate_ap_hash_from_bytes(hash_entry.test_bytes)
        test_result_str = convert_int_to_hex_string(test_result)
        assert test_result == hash_entry.expected_int
        assert test_result_str == hash_entry.expected_str


# fmt: on
