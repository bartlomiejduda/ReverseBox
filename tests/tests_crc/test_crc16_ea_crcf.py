"""
Copyright © 2024  Bartłomiej Duda
License: GPL-3.0 License
"""

import pytest

from reversebox.common.common import convert_int_to_hex_string
from reversebox.crc.crc16_ea_crcf import CRCEACRCFHandler
from tests.common import CRCTestEntry

crc_ea_crcf_handler = CRCEACRCFHandler()


@pytest.mark.unittest
def test_crc_calculate_crc16_ea_crcf_to_match_expected_result():
    crc_data_list = [
        CRCTestEntry(test_data=b"123456789", expected_int=10436, expected_str="0x28C4"),
        CRCTestEntry(test_data=b"123", expected_int=32358, expected_str="0x7E66"),
        CRCTestEntry(test_data=b"abcd", expected_int=53458, expected_str="0xD0D2"),
        CRCTestEntry(
            test_data=b"Secret123@123", expected_int=8315, expected_str="0x207B"
        ),
        CRCTestEntry(test_data=b"", expected_int=64490, expected_str="0xFBEA"),
        CRCTestEntry(test_data=b" ", expected_int=22395, expected_str="0x577B"),
        CRCTestEntry(test_data=b"\xAA\xBB", expected_int=12336, expected_str="0x3030"),
        CRCTestEntry(
            test_data=b"\x01\x02\x03\x04", expected_int=59108, expected_str="0xE6E4"
        ),
    ]

    for crc_entry in crc_data_list:
        # check expected result from first execution
        test_result = crc_ea_crcf_handler.calculate_crc16_ea_crcf(crc_entry.test_data)
        test_result_str = convert_int_to_hex_string(test_result)
        assert test_result == crc_entry.expected_int
        assert test_result_str == crc_entry.expected_str

        # check if result is the same after second execution
        test_result = crc_ea_crcf_handler.calculate_crc16_ea_crcf(crc_entry.test_data)
        test_result_str = convert_int_to_hex_string(test_result)
        assert test_result == crc_entry.expected_int
        assert test_result_str == crc_entry.expected_str
