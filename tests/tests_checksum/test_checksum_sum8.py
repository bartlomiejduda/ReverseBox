"""
Copyright © 2024  Bartłomiej Duda
License: GPL-3.0 License
"""

import pytest

from reversebox.checksum.checksum_sum8 import Sum8Handler
from reversebox.common.common import convert_int_to_hex_string
from tests.common import CRCTestEntry

sum8_handler = Sum8Handler()

# fmt: off



@pytest.mark.unittest
def test_checksum_calculate_sum8_to_match_expected_result():
    crc_data_list = [
        CRCTestEntry(test_data=b"Hello", expected_int=244, expected_str="0xF4"),
        CRCTestEntry(test_data=b"abcd", expected_int=138, expected_str="0x8A"),
        CRCTestEntry(test_data=b"Secret123@123", expected_int=210, expected_str="0xD2"),
        CRCTestEntry(test_data=b"\x01\x02\x03\x04\x05", expected_int=15, expected_str="0x0F"),
        CRCTestEntry(test_data=b"", expected_int=0, expected_str="0x00"),
        CRCTestEntry(test_data=b" ", expected_int=32, expected_str="0x20"),
        CRCTestEntry(test_data=b"ZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZ", expected_int=140, expected_str="0x8C"),
    ]

    for crc_entry in crc_data_list:
        # check expected result from first execution
        test_result = sum8_handler.calculate_sum8(crc_entry.test_data)
        test_result_str = convert_int_to_hex_string(test_result)
        assert test_result == crc_entry.expected_int
        assert test_result_str == crc_entry.expected_str

        # check if result is the same after second execution
        test_result = sum8_handler.calculate_sum8(crc_entry.test_data)
        test_result_str = convert_int_to_hex_string(test_result)
        assert test_result == crc_entry.expected_int
        assert test_result_str == crc_entry.expected_str

# fmt: on
