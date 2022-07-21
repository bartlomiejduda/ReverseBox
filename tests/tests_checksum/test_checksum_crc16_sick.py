"""
Copyright © 2022  Bartłomiej Duda
License: GPL-3.0 License
"""

import pytest
from reversebox.checksum.checksum_crc16_sick import CRC16SICKHandler
from reversebox.common.common import convert_int_to_hex_string
from tests.common import CRCTestEntry

crc16_sick_handler = CRC16SICKHandler()


@pytest.mark.unittest
def test_checksum_calculate_crc16_sick_to_match_expected_result():
    crc_data_list = [
        CRCTestEntry(test_data=b"123456789", expected_int=22182, expected_str="0x56A6"),
        CRCTestEntry(test_data=b"123", expected_int=37712, expected_str="0x9350"),
        CRCTestEntry(test_data=b"", expected_int=0, expected_str="0x00"),
        CRCTestEntry(test_data=b" ", expected_int=8192, expected_str="0x2000"),
        CRCTestEntry(test_data=b"\xAA\xBB", expected_int=61355, expected_str="0xEFAB"),
        CRCTestEntry(
            test_data=b"\x01\x02\x03\x04", expected_int=515, expected_str="0x203"
        ),
    ]

    for crc_entry in crc_data_list:
        # check expected result from first execution
        test_result = crc16_sick_handler.calculate_crc16_sick(crc_entry.test_data)
        test_result_str = convert_int_to_hex_string(test_result)
        assert test_result == crc_entry.expected_int
        assert test_result_str == crc_entry.expected_str

        # check if result is the same after second execution
        test_result = crc16_sick_handler.calculate_crc16_sick(crc_entry.test_data)
        test_result_str = convert_int_to_hex_string(test_result)
        assert test_result == crc_entry.expected_int
        assert test_result_str == crc_entry.expected_str
