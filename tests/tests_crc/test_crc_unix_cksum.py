"""
Copyright © 2024  Bartłomiej Duda
License: GPL-3.0 License
"""

import pytest

from reversebox.common.common import convert_int_to_hex_string
from reversebox.crc.crc_unix_cksum import CRCUnixCKSumHandler
from tests.common import CRCTestEntry

crc_unix_cksum_handler = CRCUnixCKSumHandler()


@pytest.mark.unittest
def test_crc_calculate_crc_unix_cksum_to_match_expected_result():
    crc_data_list = [
        CRCTestEntry(
            test_data=b"123456789", expected_int=930766865, expected_str="0x377A6011"
        ),
        CRCTestEntry(
            test_data=b"123", expected_int=1411111867, expected_str="0x541BDBBB"
        ),
        CRCTestEntry(test_data=b"", expected_int=4294967295, expected_str="0xFFFFFFFF"),
        CRCTestEntry(
            test_data=b" ", expected_int=3684553838, expected_str="0xDB9DD46E"
        ),
        CRCTestEntry(
            test_data=b"\xAA\xBB", expected_int=1721189355, expected_str="0x669743EB"
        ),
        CRCTestEntry(
            test_data=b"\x01\x02\x03\x04",
            expected_int=1587614295,
            expected_str="0x5EA11257",
        ),
    ]

    for crc_entry in crc_data_list:
        # check expected result from first execution
        test_result = crc_unix_cksum_handler.calculate_crc_cksum(crc_entry.test_data)
        test_result_str = convert_int_to_hex_string(test_result)
        assert test_result == crc_entry.expected_int
        assert test_result_str == crc_entry.expected_str

        # check if result is the same after second execution
        test_result = crc_unix_cksum_handler.calculate_crc_cksum(crc_entry.test_data)
        test_result_str = convert_int_to_hex_string(test_result)
        assert test_result == crc_entry.expected_int
        assert test_result_str == crc_entry.expected_str
