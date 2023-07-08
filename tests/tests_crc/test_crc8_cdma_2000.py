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
def test_crc_calculate_crc8_cdma_2000_to_match_expected_result():
    crc_data_list = [
        CRCTestEntry(test_data=b"abcd", expected_int=13, expected_str="0x0D"),
        CRCTestEntry(test_data=b"123456789", expected_int=218, expected_str="0xDA"),
        CRCTestEntry(test_data=b"123", expected_int=23, expected_str="0x17"),
        CRCTestEntry(test_data=b"Secret123@456", expected_int=210, expected_str="0xD2"),
        CRCTestEntry(test_data=b"", expected_int=255, expected_str="0xFF"),
        CRCTestEntry(test_data=b" ", expected_int=31, expected_str="0x1F"),
        CRCTestEntry(test_data=b"\xAA\xBB", expected_int=29, expected_str="0x1D"),
        CRCTestEntry(
            test_data=b"\x01\x02\x03\x04", expected_int=103, expected_str="0x67"
        ),
        CRCTestEntry(test_data=b"!@#$%^&*()", expected_int=167, expected_str="0xA7"),
    ]

    for crc_entry in crc_data_list:
        # check expected result from first execution
        test_result = crc8_handler.calculate_crc8_cdma_2000(crc_entry.test_data)
        test_result_str = convert_int_to_hex_string(test_result)
        assert test_result == crc_entry.expected_int
        assert test_result_str == crc_entry.expected_str

        # check if result is the same after second execution
        test_result = crc8_handler.calculate_crc8_cdma_2000(crc_entry.test_data)
        test_result_str = convert_int_to_hex_string(test_result)
        assert test_result == crc_entry.expected_int
        assert test_result_str == crc_entry.expected_str
