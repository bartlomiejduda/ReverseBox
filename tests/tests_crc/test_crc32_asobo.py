"""
Copyright © 2023  Bartłomiej Duda
License: GPL-3.0 License
"""

import pytest

from reversebox.common.common import convert_int_to_hex_string
from reversebox.crc.crc32_asobo import CRC32AsoboHandler
from tests.common import CRCTestEntry

crc32_asobo_handler = CRC32AsoboHandler()


@pytest.mark.unittest
def test_crc_calculate_crc32_asobo_to_match_expected_result():
    crc_data_list = [
        CRCTestEntry(
            test_data=b"abcd", expected_int=2161055104, expected_str="0x80CF1580"
        ),
        CRCTestEntry(
            test_data=b"123456789", expected_int=4027864427, expected_str="0xF014556B"
        ),
        CRCTestEntry(
            test_data=b"123", expected_int=1589920508, expected_str="0x5EC442FC"
        ),
        CRCTestEntry(
            test_data=b"Secret123@456",
            expected_int=3452879509,
            expected_str="0xCDCEC295",
        ),
        CRCTestEntry(test_data=b"", expected_int=0, expected_str="0x00"),
        CRCTestEntry(
            test_data=b" ", expected_int=2552477408, expected_str="0x9823B6E0"
        ),
        CRCTestEntry(
            test_data=b"\xAA\xBB", expected_int=2704819662, expected_str="0xA13845CE"
        ),
        CRCTestEntry(
            test_data=b"\x01\x02\x03\x04",
            expected_int=1026533933,
            expected_str="0x3D2FAA2D",
        ),
        CRCTestEntry(
            test_data=b"!@#$%^&*()", expected_int=2350173499, expected_str="0x8C14CD3B"
        ),
    ]

    for crc_entry in crc_data_list:
        # check expected result from first execution
        test_result = crc32_asobo_handler.calculate_crc32_asobo(crc_entry.test_data)
        test_result_str = convert_int_to_hex_string(test_result)
        assert test_result == crc_entry.expected_int
        assert test_result_str == crc_entry.expected_str

        # check if result is the same after second execution
        test_result = crc32_asobo_handler.calculate_crc32_asobo(crc_entry.test_data)
        test_result_str = convert_int_to_hex_string(test_result)
        assert test_result == crc_entry.expected_int
        assert test_result_str == crc_entry.expected_str
