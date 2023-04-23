"""
Copyright © 2022  Bartłomiej Duda
License: GPL-3.0 License
"""

import zlib

import pytest
from faker import Faker

from reversebox.common.common import convert_int_to_hex_string
from reversebox.crc.crc32_iso_hdlc import CRC32Handler
from tests.common import CRCTestEntry

crc32_handler = CRC32Handler()
fake = Faker()


@pytest.mark.unittest
def test_crc_calculate_crc32_iso_hdlc_to_match_expected_result():
    crc_data_list = [
        CRCTestEntry(
            test_data=b"123456789", expected_int=3421780262, expected_str="0xCBF43926"
        ),
        CRCTestEntry(
            test_data=b"123", expected_int=2286445522, expected_str="0x884863D2"
        ),
        CRCTestEntry(test_data=b"", expected_int=0, expected_str="0x00"),
        CRCTestEntry(
            test_data=b" ", expected_int=3916222277, expected_str="0xE96CCF45"
        ),
        CRCTestEntry(
            test_data=b"\xAA\xBB", expected_int=1233267864, expected_str="0x49822C98"
        ),
        CRCTestEntry(
            test_data=b"\x01\x02\x03\x04",
            expected_int=3057449933,
            expected_str="0xB63CFBCD",
        ),
    ]

    for crc_entry in crc_data_list:
        # check expected result from first execution
        test_result = crc32_handler.calculate_crc32(crc_entry.test_data)
        test_result_str = convert_int_to_hex_string(test_result)
        assert test_result == crc_entry.expected_int
        assert test_result_str == crc_entry.expected_str

        # check if result is the same after second execution
        test_result = crc32_handler.calculate_crc32(crc_entry.test_data)
        test_result_str = convert_int_to_hex_string(test_result)
        assert test_result == crc_entry.expected_int
        assert test_result_str == crc_entry.expected_str


@pytest.mark.unittest
def test_crc_calculate_crc32_iso_hdlc_to_match_zlib_result():
    test_data_array = [
        b"",
        b" ",
        b"123456789",
        b"123",
        b"Hello Python",
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
        test_result = crc32_handler.calculate_crc32(test_data)
        zlib_result = zlib.crc32(test_data)
        test_result_str = convert_int_to_hex_string(test_result)
        zlib_result_str = convert_int_to_hex_string(zlib_result)
        assert test_result == zlib_result
        assert test_result_str == zlib_result_str
