"""
Copyright © 2022  Bartłomiej Duda
License: GPL-3.0 License
"""

import pytest

from reversebox.common.common import convert_int_to_hex_string
from reversebox.crc.crc16_modbus import CRC16MODBUSHandler
from tests.common import CRCTestEntry

crc16_modbus_handler = CRC16MODBUSHandler()

# fmt: off


@pytest.mark.unittest
def test_crc_calculate_crc16_modbus_to_match_expected_result():
    crc_data_list = [
        CRCTestEntry(test_data=b"123456789", expected_int=19255, expected_str="0x4B37"),
        CRCTestEntry(test_data=b"123", expected_int=31349, expected_str="0x7A75"),
        CRCTestEntry(test_data=b"abcd", expected_int=7575, expected_str="0x1D97"),
        CRCTestEntry(test_data=b"Secret123@123", expected_int=31416, expected_str="0x7AB8"),
        CRCTestEntry(test_data=b"", expected_int=65535, expected_str="0xFFFF"),
        CRCTestEntry(test_data=b" ", expected_int=39102, expected_str="0x98BE"),
        CRCTestEntry(test_data=b"\xAA\xBB", expected_int=25407, expected_str="0x633F"),
        CRCTestEntry(test_data=b"\x01\x02\x03\x04", expected_int=11169, expected_str="0x2BA1"),
    ]

    for crc_entry in crc_data_list:
        # check expected result from first execution
        test_result = crc16_modbus_handler.calculate_crc16_modbus(crc_entry.test_data)
        test_result_str = convert_int_to_hex_string(test_result)
        assert test_result == crc_entry.expected_int
        assert test_result_str == crc_entry.expected_str

        # check if result is the same after second execution
        test_result = crc16_modbus_handler.calculate_crc16_modbus(crc_entry.test_data)
        test_result_str = convert_int_to_hex_string(test_result)
        assert test_result == crc_entry.expected_int
        assert test_result_str == crc_entry.expected_str

# fmt: on
