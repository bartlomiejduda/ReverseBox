"""
Copyright © 2024  Bartłomiej Duda
License: GPL-3.0 License
"""

import pytest

from reversebox.common.common import convert_int_to_hex_string
from reversebox.crc.crc64_go_iso import CRC64GoISOHandler
from tests.common import CRCTestEntry

crc64_handler = CRC64GoISOHandler()


# fmt: off
@pytest.mark.unittest
def test_crc_calculate_crc64_go_iso_to_match_expected_result():
    crc_data_list = [
        CRCTestEntry(test_data=b"123456789", expected_int=13333283586479230977, expected_str="0xB90956C775A41001"),
        CRCTestEntry(test_data=b"123", expected_int=4612164443424423936, expected_str="0x4001B32000000000"),
        CRCTestEntry(test_data=b"", expected_int=0, expected_str="0x00"),
        CRCTestEntry(test_data=b" ", expected_int=6453658266021920768, expected_str="0x5990000000000000"),
        CRCTestEntry(test_data=b"\xAA\xBB", expected_int=10758941180113715200, expected_str="0x954F700000000000"),
        CRCTestEntry(test_data=b"\x01\x02\x03\x04", expected_int=7583266405215109120, expected_str="0x693D2C9E20000000"),
        CRCTestEntry(test_data=b"IHATEMATH", expected_int=2049228168195101230, expected_str="0x1C70522964FE522E")
    ]

    for crc_entry in crc_data_list:
        # check expected result from first execution
        test_result = crc64_handler.calculate_crc64(crc_entry.test_data)
        test_result_str = convert_int_to_hex_string(test_result)
        assert test_result == crc_entry.expected_int
        assert test_result_str == crc_entry.expected_str

        # check if result is the same after second execution
        test_result = crc64_handler.calculate_crc64(crc_entry.test_data)
        test_result_str = convert_int_to_hex_string(test_result)
        assert test_result == crc_entry.expected_int
        assert test_result_str == crc_entry.expected_str

# fmt: on
