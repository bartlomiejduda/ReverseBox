"""
Copyright © 2022  Bartłomiej Duda
License: GPL-3.0 License
"""

import pytest
from reversebox.checksum.checksum_crc16_dnp import CRC16DNPHandler
from reversebox.common.common import convert_int_to_hex_string
from tests.common import CRCTestEntry

crc16_dnp_handler = CRC16DNPHandler()


@pytest.mark.unittest
def test_checksum_calculate_crc16_dnp_to_match_expected_result():
    crc_data_list = [
        # CRCTestEntry(test_data=b"123456789", expected_int=35105, expected_str="0x8921"),
        # CRCTestEntry(test_data=b'123', expected_int=30810, expected_str="0x785A"),
        # CRCTestEntry(test_data=b'', expected_int=0, expected_str="0x00"),
        # CRCTestEntry(test_data=b' ', expected_int=545, expected_str="0x221"),
        # CRCTestEntry(test_data=b'\xAA\xBB', expected_int=55129, expected_str="0xD759"),
        # CRCTestEntry(test_data=b'\x01\x02\x03\x04', expected_int=20421, expected_str="0x4FC5"),
    ]

    for crc_entry in crc_data_list:
        # check expected result from first execution
        test_result = crc16_dnp_handler.calculate_crc16_dnp(crc_entry.test_data)
        test_result_str = convert_int_to_hex_string(test_result)
        assert test_result == crc_entry.expected_int
        assert test_result_str == crc_entry.expected_str

        # check if result is the same after second execution
        test_result = crc16_dnp_handler.calculate_crc16_dnp(crc_entry.test_data)
        test_result_str = convert_int_to_hex_string(test_result)
        assert test_result == crc_entry.expected_int
        assert test_result_str == crc_entry.expected_str
