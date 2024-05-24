"""
Copyright © 2024  Bartłomiej Duda
License: GPL-3.0 License
"""

import pytest

from reversebox.checksum.checksum_xor8 import Xor8Handler
from reversebox.common.common import convert_int_to_hex_string
from tests.common import CRCTestEntry

xor8_handler = Xor8Handler()

# fmt: off



@pytest.mark.unittest
def test_checksum_calculate_xor8_to_match_expected_result():
    crc_data_list = [
        CRCTestEntry(test_data=b"123456789", expected_int=49, expected_str="0x31"),
        CRCTestEntry(test_data=b"Hello", expected_int=66, expected_str="0x42"),
        CRCTestEntry(test_data=b"abcd", expected_int=4, expected_str="0x04"),
        CRCTestEntry(test_data=b"Secret123@123", expected_int=118, expected_str="0x76"),
        CRCTestEntry(test_data=b"\x01\x02\x03\x04\x05", expected_int=1, expected_str="0x01"),
        CRCTestEntry(test_data=b"", expected_int=0, expected_str="0x00"),
        CRCTestEntry(test_data=b" ", expected_int=32, expected_str="0x20"),
        CRCTestEntry(test_data=b"ZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZ", expected_int=0, expected_str="0x00"),
    ]

    for crc_entry in crc_data_list:
        # check expected result from first execution
        test_result = xor8_handler.calculate_xor8(crc_entry.test_data)
        test_result_str = convert_int_to_hex_string(test_result)
        assert test_result == crc_entry.expected_int
        assert test_result_str == crc_entry.expected_str

        # check if result is the same after second execution
        test_result = xor8_handler.calculate_xor8(crc_entry.test_data)
        test_result_str = convert_int_to_hex_string(test_result)
        assert test_result == crc_entry.expected_int
        assert test_result_str == crc_entry.expected_str

# fmt: on
