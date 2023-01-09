"""
Copyright © 2023  Bartłomiej Duda
License: GPL-3.0 License
"""

import pytest

from reversebox.checksum.checksum_fletcher16 import Fletcher16Handler
from reversebox.common.common import convert_int_to_hex_string
from tests.common import CRCTestEntry

fletcher16_handler = Fletcher16Handler()

# fmt: off


@pytest.mark.unittest
def test_checksum_calculate_fletcher16_to_match_expected_result():
    crc_data_list = [
        CRCTestEntry(test_data=b"abcd", expected_int=55179, expected_str="0xD78B"),
        CRCTestEntry(test_data=b"123456789", expected_int=7902, expected_str="0x1EDE"),
        CRCTestEntry(test_data=b"123", expected_int=11158, expected_str="0x2B96"),
        CRCTestEntry(test_data=b"Secret123@456", expected_int=45534, expected_str="0xB1DE"),
        CRCTestEntry(test_data=b"", expected_int=0, expected_str="0x00"),
        CRCTestEntry(test_data=b" ", expected_int=8224, expected_str="0x2020"),
        CRCTestEntry(test_data=b"\xAA\xBB", expected_int=4454, expected_str="0x1166"),
        CRCTestEntry(test_data=b"\x01\x02\x03\x04", expected_int=5130, expected_str="0x140A"),
    ]

    for crc_entry in crc_data_list:
        # check expected result from first execution
        test_result = fletcher16_handler.calculate_fletcher16(crc_entry.test_data)
        test_result_str = convert_int_to_hex_string(test_result)
        assert test_result == crc_entry.expected_int
        assert test_result_str == crc_entry.expected_str

        # check if result is the same after second execution
        test_result = fletcher16_handler.calculate_fletcher16(crc_entry.test_data)
        test_result_str = convert_int_to_hex_string(test_result)
        assert test_result == crc_entry.expected_int
        assert test_result_str == crc_entry.expected_str
