"""
Copyright © 2024  Bartłomiej Duda
License: GPL-3.0 License
"""

import pytest

from reversebox.checksum.checksum_internet_ipv4_header import (
    InternetIPv4headerChecksumHandler,
)
from reversebox.common.common import convert_int_to_hex_string
from tests.common import CRCTestEntry

internet_ipv4_header_handler = InternetIPv4headerChecksumHandler()

# fmt: off


ipv4_header = bytearray(20)
ipv4_header[0] = 0x45
ipv4_header[1] = 0x00
ipv4_header[2] = 0x00
ipv4_header[3] = 0xe8
ipv4_header[4] = 0x00
ipv4_header[5] = 0x00
ipv4_header[6] = 0x40
ipv4_header[7] = 0x00
ipv4_header[8] = 0x40
ipv4_header[9] = 0x11
ipv4_header[10] = 0x0
ipv4_header[11] = 0x0
ipv4_header[12] = 0x0a
ipv4_header[13] = 0x86
ipv4_header[14] = 0x33
ipv4_header[15] = 0xf1
ipv4_header[16] = 0x0a
ipv4_header[17] = 0x86
ipv4_header[18] = 0x33
ipv4_header[19] = 0x76


@pytest.mark.unittest
def test_checksum_calculate_internet_ipv4_header_to_match_expected_result():
    crc_data_list = [
        CRCTestEntry(test_data=ipv4_header, expected_int=37565, expected_str="0x92BD"),
        CRCTestEntry(test_data=b"\x00\x01\xf2\x03\xf4\xf5\xf6\xf7", expected_int=3362, expected_str="0xD22"),
        CRCTestEntry(test_data=b"\xe3\x4f\x23\x96\x44\x27\x99\xf3", expected_int=65306, expected_str="0xFF1A"),  # http://kfall.net/ucbpage/EE122/lec06/sld023.htm
        CRCTestEntry(test_data=b"\x45\x00\x00\x73\x00\x00\x40\x00\x40\x11\xc0\xa8\x00\x01\xc0\xa8\x00\xc7", expected_int=25016, expected_str="0x61B8"),  # https://en.wikipedia.org/wiki/Internet_checksum
        CRCTestEntry(test_data=b"123456789", expected_int=10998, expected_str="0x2AF6"),
        CRCTestEntry(test_data=b"Hello", expected_int=11740, expected_str="0x2DDC"),
        CRCTestEntry(test_data=b"abcd", expected_int=14651, expected_str="0x393B"),
        CRCTestEntry(test_data=b"Secret123@123", expected_int=3867, expected_str="0xF1B"),
        CRCTestEntry(test_data=b"\x01\x02\x03\x04\x05", expected_int=63990, expected_str="0xF9F6"),
        CRCTestEntry(test_data=b"", expected_int=65535, expected_str="0xFFFF"),
        CRCTestEntry(test_data=b" ", expected_int=65503, expected_str="0xFFDF"),
        CRCTestEntry(test_data=b"ZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZ", expected_int=46260, expected_str="0xB4B4"),
    ]

    for crc_entry in crc_data_list:
        # check expected result from first execution
        test_result = internet_ipv4_header_handler.calculate_internet_ipv4_header_checksum(crc_entry.test_data)
        test_result_str = convert_int_to_hex_string(test_result)
        assert test_result == crc_entry.expected_int
        assert test_result_str == crc_entry.expected_str

        # check if result is the same after second execution
        test_result = internet_ipv4_header_handler.calculate_internet_ipv4_header_checksum(crc_entry.test_data)
        test_result_str = convert_int_to_hex_string(test_result)
        assert test_result == crc_entry.expected_int
        assert test_result_str == crc_entry.expected_str

# fmt: on
