"""
Copyright © 2023  Bartłomiej Duda
License: GPL-3.0 License
"""

import pytest
from faker import Faker

from reversebox.checksum.checksum_bsd16 import BSD16Handler
from reversebox.common.common import convert_int_to_hex_string
from tests.common import CRCTestEntry

bsd16_handler = BSD16Handler()
fake = Faker()

# fmt: off


@pytest.mark.unittest
def test_checksum_calculate_bsd16_to_match_expected_result():
    crc_data_list = [
        CRCTestEntry(test_data=b"abcd", expected_int=8378, expected_str="0x20BA"),
        CRCTestEntry(test_data=b"123456789", expected_int=53615, expected_str="0xD16F"),
        CRCTestEntry(test_data=b"123", expected_int=16472, expected_str="0x4058"),
        CRCTestEntry(test_data=b"Secret123@456", expected_int=46332, expected_str="0xB4FC"),
        CRCTestEntry(test_data=b"", expected_int=0, expected_str="0x00"),
        CRCTestEntry(test_data=b" ", expected_int=32, expected_str="0x20"),
        CRCTestEntry(test_data=b"\xAA\xBB", expected_int=272, expected_str="0x110"),
        CRCTestEntry(test_data=b"\x01\x02\x03\x04", expected_int=8198, expected_str="0x2006"),
        CRCTestEntry(test_data=b"!@#$%^&*()", expected_int=28372, expected_str="0x6ED4"),
    ]

    for crc_entry in crc_data_list:
        # check expected result from first execution
        test_result = bsd16_handler.calculate_bsd16(crc_entry.test_data)
        test_result_str = convert_int_to_hex_string(test_result)
        assert test_result == crc_entry.expected_int
        assert test_result_str == crc_entry.expected_str

        # check if result is the same after second execution
        test_result = bsd16_handler.calculate_bsd16(crc_entry.test_data)
        test_result_str = convert_int_to_hex_string(test_result)
        assert test_result == crc_entry.expected_int
        assert test_result_str == crc_entry.expected_str

# fmt: on
