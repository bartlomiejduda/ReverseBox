"""
Copyright © 2024  Bartłomiej Duda
License: GPL-3.0 License
"""

import pytest

from reversebox.checksum.checksum_sum8_2s_complement import Sum82sComplementHandler
from reversebox.common.common import convert_int_to_hex_string
from tests.common import CRCTestEntry

sum8_2s_complement_handler = Sum82sComplementHandler()

# fmt: off



@pytest.mark.unittest
def test_checksum_calculate_sum8_2s_complement_to_match_expected_result():
    crc_data_list = [
        CRCTestEntry(test_data=b"123456789", expected_int=35, expected_str="0x23"),
        CRCTestEntry(test_data=b"Hello", expected_int=12, expected_str="0x0C"),
        CRCTestEntry(test_data=b"abcd", expected_int=118, expected_str="0x76"),
        CRCTestEntry(test_data=b"Secret123@123", expected_int=46, expected_str="0x2E"),
        CRCTestEntry(test_data=b"\x01\x02\x03\x04\x05", expected_int=241, expected_str="0xF1"),
        CRCTestEntry(test_data=b"", expected_int=0, expected_str="0x00"),
        CRCTestEntry(test_data=b" ", expected_int=224, expected_str="0xE0"),
        CRCTestEntry(test_data=b"ZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZ", expected_int=116, expected_str="0x74"),
    ]

    for crc_entry in crc_data_list:
        # check expected result from first execution
        test_result = sum8_2s_complement_handler.calculate_sum8_2s_complement(crc_entry.test_data)
        test_result_str = convert_int_to_hex_string(test_result)
        assert test_result == crc_entry.expected_int
        assert test_result_str == crc_entry.expected_str

        # check if result is the same after second execution
        test_result = sum8_2s_complement_handler.calculate_sum8_2s_complement(crc_entry.test_data)
        test_result_str = convert_int_to_hex_string(test_result)
        assert test_result == crc_entry.expected_int
        assert test_result_str == crc_entry.expected_str

# fmt: on
