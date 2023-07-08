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
def test_crc_calculate_crc8_darc_to_match_expected_result():
    crc_data_list = [
        CRCTestEntry(test_data=b"abcd", expected_int=192, expected_str="0xC0"),
        CRCTestEntry(test_data=b"123456789", expected_int=21, expected_str="0x15"),
        CRCTestEntry(test_data=b"123", expected_int=215, expected_str="0xD7"),
        CRCTestEntry(test_data=b"Secret123@456", expected_int=180, expected_str="0xB4"),
        CRCTestEntry(test_data=b"", expected_int=0, expected_str="0x00"),
        CRCTestEntry(test_data=b" ", expected_int=39, expected_str="0x27"),
        CRCTestEntry(test_data=b"\xAA\xBB", expected_int=20, expected_str="0x14"),
        CRCTestEntry(
            test_data=b"\x01\x02\x03\x04", expected_int=2, expected_str="0x02"
        ),
        CRCTestEntry(test_data=b"!@#$%^&*()", expected_int=255, expected_str="0xFF"),
    ]

    for crc_entry in crc_data_list:
        # check expected result from first execution
        test_result = crc8_handler.calculate_crc8_darc(crc_entry.test_data)
        test_result_str = convert_int_to_hex_string(test_result)
        assert test_result == crc_entry.expected_int
        assert test_result_str == crc_entry.expected_str

        # check if result is the same after second execution
        test_result = crc8_handler.calculate_crc8_darc(crc_entry.test_data)
        test_result_str = convert_int_to_hex_string(test_result)
        assert test_result == crc_entry.expected_int
        assert test_result_str == crc_entry.expected_str
