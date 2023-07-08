"""
Copyright © 2023  Bartłomiej Duda
License: GPL-3.0 License
"""

import pytest

from reversebox.common.common import convert_int_to_hex_string
from reversebox.crc.crc8 import CRC8Handler
from tests.common import CRCTestEntry

crc8_handler = CRC8Handler()


@pytest.mark.unittest
def test_crc_calculate_crc8_to_match_expected_result():
    crc_data_list = [
        CRCTestEntry(test_data=b"abcd", expected_int=161, expected_str="0xA1"),
        CRCTestEntry(test_data=b"123456789", expected_int=244, expected_str="0xF4"),
        CRCTestEntry(test_data=b"123", expected_int=192, expected_str="0xC0"),
        CRCTestEntry(test_data=b"Secret123@456", expected_int=154, expected_str="0x9A"),
        CRCTestEntry(test_data=b"", expected_int=0, expected_str="0x00"),
        CRCTestEntry(test_data=b" ", expected_int=224, expected_str="0xE0"),
        CRCTestEntry(test_data=b"\xAA\xBB", expected_int=178, expected_str="0xB2"),
        CRCTestEntry(
            test_data=b"\x01\x02\x03\x04", expected_int=227, expected_str="0xE3"
        ),
        CRCTestEntry(test_data=b"!@#$%^&*()", expected_int=103, expected_str="0x67"),
    ]

    for crc_entry in crc_data_list:
        # check expected result from first execution
        test_result = crc8_handler.calculate_crc8(crc_entry.test_data)
        test_result_str = convert_int_to_hex_string(test_result)
        assert test_result == crc_entry.expected_int
        assert test_result_str == crc_entry.expected_str

        # check if result is the same after second execution
        test_result = crc8_handler.calculate_crc8(crc_entry.test_data)
        test_result_str = convert_int_to_hex_string(test_result)
        assert test_result == crc_entry.expected_int
        assert test_result_str == crc_entry.expected_str
