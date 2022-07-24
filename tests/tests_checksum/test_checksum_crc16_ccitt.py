"""
Copyright © 2022  Bartłomiej Duda
License: GPL-3.0 License
"""

import pytest
from reversebox.checksum.checksum_crc16_ccitt import CRC16CCITTHandler
from reversebox.common.common import convert_int_to_hex_string
from tests.common import CRCTestEntry

crc16_ccitt_handler = CRC16CCITTHandler()


@pytest.mark.unittest
def test_checksum_calculate_crc16_ccitt_ffff_to_match_expected_result():
    crc_data_list = [
        CRCTestEntry(test_data=b"123456789", expected_int=10673, expected_str="0x29B1"),
        CRCTestEntry(test_data=b"123", expected_int=23502, expected_str="0x5BCE"),
        CRCTestEntry(test_data=b"", expected_int=65535, expected_str="0xFFFF"),
        CRCTestEntry(test_data=b" ", expected_int=50578, expected_str="0xC592"),
        CRCTestEntry(test_data=b"\xAA\xBB", expected_int=63754, expected_str="0xF90A"),
        CRCTestEntry(
            test_data=b"\x01\x02\x03\x04", expected_int=35267, expected_str="0x89C3"
        ),
    ]

    for crc_entry in crc_data_list:
        # check expected result from first execution
        test_result = crc16_ccitt_handler.calculate_crc16_ccitt_ffff(
            crc_entry.test_data
        )
        test_result_str = convert_int_to_hex_string(test_result)
        assert test_result == crc_entry.expected_int
        assert test_result_str == crc_entry.expected_str

        # check if result is the same after second execution
        test_result = crc16_ccitt_handler.calculate_crc16_ccitt_ffff(
            crc_entry.test_data
        )
        test_result_str = convert_int_to_hex_string(test_result)
        assert test_result == crc_entry.expected_int
        assert test_result_str == crc_entry.expected_str


@pytest.mark.unittest
def test_checksum_calculate_crc16_ccitt_1d0f_to_match_expected_result():
    crc_data_list = [
        CRCTestEntry(test_data=b"123456789", expected_int=58828, expected_str="0xE5CC"),
        CRCTestEntry(test_data=b"123", expected_int=34398, expected_str="0x865E"),
        CRCTestEntry(test_data=b"", expected_int=7439, expected_str="0x1D0F"),
        CRCTestEntry(test_data=b" ", expected_int=59646, expected_str="0xE8FE"),
        CRCTestEntry(test_data=b"\xAA\xBB", expected_int=24773, expected_str="0x60C5"),
        CRCTestEntry(
            test_data=b"\x01\x02\x03\x04", expected_int=787, expected_str="0x313"
        ),
    ]

    for crc_entry in crc_data_list:
        # check expected result from first execution
        test_result = crc16_ccitt_handler.calculate_crc16_ccitt_1d0f(
            crc_entry.test_data
        )
        test_result_str = convert_int_to_hex_string(test_result)
        assert test_result == crc_entry.expected_int
        assert test_result_str == crc_entry.expected_str

        # check if result is the same after second execution
        test_result = crc16_ccitt_handler.calculate_crc16_ccitt_1d0f(
            crc_entry.test_data
        )
        test_result_str = convert_int_to_hex_string(test_result)
        assert test_result == crc_entry.expected_int
        assert test_result_str == crc_entry.expected_str


@pytest.mark.unittest
def test_checksum_calculate_crc16_ccitt_xmodem_to_match_expected_result():
    crc_data_list = [
        CRCTestEntry(test_data=b"123456789", expected_int=12739, expected_str="0x31C3"),
        CRCTestEntry(test_data=b"123", expected_int=38738, expected_str="0x9752"),
        CRCTestEntry(test_data=b"", expected_int=0, expected_str="0x00"),
        CRCTestEntry(test_data=b" ", expected_int=9314, expected_str="0x2462"),
        CRCTestEntry(test_data=b"\xAA\xBB", expected_int=58373, expected_str="0xE405"),
        CRCTestEntry(
            test_data=b"\x01\x02\x03\x04", expected_int=3331, expected_str="0xD03"
        ),
    ]

    for crc_entry in crc_data_list:
        # check expected result from first execution
        test_result = crc16_ccitt_handler.calculate_crc16_ccitt_xmodem(
            crc_entry.test_data
        )
        test_result_str = convert_int_to_hex_string(test_result)
        assert test_result == crc_entry.expected_int
        assert test_result_str == crc_entry.expected_str

        # check if result is the same after second execution
        test_result = crc16_ccitt_handler.calculate_crc16_ccitt_xmodem(
            crc_entry.test_data
        )
        test_result_str = convert_int_to_hex_string(test_result)
        assert test_result == crc_entry.expected_int
        assert test_result_str == crc_entry.expected_str
