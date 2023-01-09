"""
Copyright © 2023  Bartłomiej Duda
License: GPL-3.0 License
"""

import pytest

from reversebox.checksum.checksum_fletcher32 import Fletcher32Handler
from reversebox.common.common import convert_int_to_hex_string
from tests.common import CRCTestEntry

fletcher32_handler = Fletcher32Handler()

# fmt: off


@pytest.mark.unittest
def test_checksum_calculate_fletcher32_to_match_expected_result():
    crc_data_list = [
        CRCTestEntry(test_data=b"abcd", expected_int=690407108, expected_str="0x2926C6C4"),
        CRCTestEntry(test_data=b"123456789", expected_int=3741963529, expected_str="0xDF09D509"),
        CRCTestEntry(test_data=b"123", expected_int=1687499364, expected_str="0x64953264"),
        CRCTestEntry(test_data=b"Secret123@456", expected_int=2912220138, expected_str="0xAD94F3EA"),
        CRCTestEntry(test_data=b"", expected_int=0, expected_str="0x00"),
        CRCTestEntry(test_data=b" ", expected_int=2097184, expected_str="0x200020"),
        CRCTestEntry(test_data=b"\xAA\xBB", expected_int=3148528554, expected_str="0xBBAABBAA"),
        CRCTestEntry(test_data=b"\x01\x02\x03\x04", expected_int=134546948, expected_str="0x8050604"),
    ]

    for crc_entry in crc_data_list:
        # check expected result from first execution
        test_result = fletcher32_handler.calculate_fletcher32(crc_entry.test_data)
        test_result_str = convert_int_to_hex_string(test_result)
        assert test_result == crc_entry.expected_int
        assert test_result_str == crc_entry.expected_str

        # check if result is the same after second execution
        test_result = fletcher32_handler.calculate_fletcher32(crc_entry.test_data)
        test_result_str = convert_int_to_hex_string(test_result)
        assert test_result == crc_entry.expected_int
        assert test_result_str == crc_entry.expected_str
