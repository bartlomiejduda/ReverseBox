"""
Copyright © 2022  Bartłomiej Duda
License: GPL-3.0 License
"""

import pytest

from reversebox.checksum.checksum_crc16_arc import CRC16Handler
from reversebox.common.common import convert_int_to_hex_string
from tests.common import CRCTestEntry

crc16_handler = CRC16Handler()


@pytest.mark.unittest
def test_checksum_calculate_crc16_to_match_expected_result():
    crc_data_list = [
        CRCTestEntry(test_data=b"123456789", expected_int=47933, expected_str="0xBB3D"),
        CRCTestEntry(test_data=b"123", expected_int=47620, expected_str="0xBA04"),
        CRCTestEntry(
            test_data=b"Hello Python", expected_int=44785, expected_str="0xAEF1"
        ),
        CRCTestEntry(
            test_data=b"Secret123@123", expected_int=37307, expected_str="0x91BB"
        ),
        CRCTestEntry(test_data=b"abcdefgh", expected_int=29737, expected_str="0x7429"),
        CRCTestEntry(test_data=b"ABCDEFGH", expected_int=7070, expected_str="0x1B9E"),
        CRCTestEntry(test_data=b"@@@@@", expected_int=60197, expected_str="0xEB25"),
        CRCTestEntry(
            test_data=b"C:\\Users\\user\\Desktop\\audio.wav",
            expected_int=40361,
            expected_str="0x9DA9",
        ),
        CRCTestEntry(
            test_data=b"/etc/passwd", expected_int=15164, expected_str="0x3B3C"
        ),
        CRCTestEntry(test_data=b" ", expected_int=55297, expected_str="0xD801"),
        CRCTestEntry(test_data=b"\xAA\xBB", expected_int=54078, expected_str="0xD33E"),
        CRCTestEntry(
            test_data=b"\x01\x02\x03\x04", expected_int=4001, expected_str="0xFA1"
        ),
    ]

    for crc_entry in crc_data_list:
        # check expected result from first execution
        test_result = crc16_handler.calculate_crc16(crc_entry.test_data)
        test_result_str = convert_int_to_hex_string(test_result)
        assert test_result == crc_entry.expected_int
        assert test_result_str == crc_entry.expected_str

        # check if result is the same after second execution
        test_result = crc16_handler.calculate_crc16(crc_entry.test_data)
        test_result_str = convert_int_to_hex_string(test_result)
        assert test_result == crc_entry.expected_int
        assert test_result_str == crc_entry.expected_str
