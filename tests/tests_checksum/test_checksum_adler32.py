"""
Copyright © 2023  Bartłomiej Duda
License: GPL-3.0 License
"""

import zlib

import pytest
from faker import Faker

from reversebox.checksum.checksum_adler32 import Adler32Handler
from reversebox.common.common import convert_int_to_hex_string
from tests.common import CRCTestEntry

adler32_handler = Adler32Handler()
fake = Faker()

# fmt: off


@pytest.mark.unittest
def test_checksum_calculate_adler32_to_match_expected_result():
    crc_data_list = [
        CRCTestEntry(test_data=b"abcd", expected_int=64487819, expected_str="0x3D8018B"),
        CRCTestEntry(test_data=b"123456789", expected_int=152961502, expected_str="0x91E01DE"),
        CRCTestEntry(test_data=b"123", expected_int=19726487, expected_str="0x12D0097"),
        CRCTestEntry(test_data=b"Secret123@456", expected_int=513803228, expected_str="0x1EA003DC"),
        CRCTestEntry(test_data=b"", expected_int=1, expected_str="0x01"),
        CRCTestEntry(test_data=b" ", expected_int=2162721, expected_str="0x210021"),
        CRCTestEntry(test_data=b"\xAA\xBB", expected_int=34668902, expected_str="0x2110166"),
        CRCTestEntry(test_data=b"\x01\x02\x03\x04", expected_int=1572875, expected_str="0x18000B"),
    ]

    for crc_entry in crc_data_list:
        # check expected result from first execution
        test_result = adler32_handler.calculate_adler32(crc_entry.test_data)
        test_result_str = convert_int_to_hex_string(test_result)
        assert test_result == crc_entry.expected_int
        assert test_result_str == crc_entry.expected_str

        # check if result is the same after second execution
        test_result = adler32_handler.calculate_adler32(crc_entry.test_data)
        test_result_str = convert_int_to_hex_string(test_result)
        assert test_result == crc_entry.expected_int
        assert test_result_str == crc_entry.expected_str


@pytest.mark.unittest
def test_checksum_calculate_adler32_to_match_zlib_result():

    test_data_array = [
        b"",
        b" ",
        b"123456789",
        b"123",
        b"Hello Python",
        b"Secret123@456",
        b"Secret123@123#!",
        b"\xAA\xBB",
        b"\x00\x01\x02\x03",
        b"1",
        b"abcdefgh",
        b"\n",
        b"!@#$%^&*()",
        fake.binary(length=100),
        fake.binary(length=5000),
    ]

    for test_data in test_data_array:
        test_result = adler32_handler.calculate_adler32(test_data)
        adler_result = zlib.adler32(test_data)
        test_result_str = convert_int_to_hex_string(test_result)
        adler_result_str = convert_int_to_hex_string(adler_result)
        assert test_result == adler_result
        assert test_result_str == adler_result_str

# fmt: on
