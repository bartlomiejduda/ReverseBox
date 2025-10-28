"""
Copyright © 2025 Bartłomiej Duda
License: GPL-3.0 License
"""

import pytest

from reversebox.common.common import convert_int_to_hex_string
from reversebox.hash.hash_rx3 import RX3HashHandler
from tests.common import BytesHashTestEntry, TextHashTestEntry

rx3_handler = RX3HashHandler()


# fmt: off

@pytest.mark.unittest
def test_hash_rx3_from_string_to_match_expected_result():
    hash_data_list = [
        TextHashTestEntry(test_string="texturebatch", expected_int=1808827868, expected_str="0x6BD085DC", hash_size=4),
        TextHashTestEntry(test_string="texture", expected_int=2047566042, expected_str="0x7A0B60DA", hash_size=4),
        TextHashTestEntry(test_string="ib", expected_int=5798132, expected_str="0x5878F4", hash_size=4),
        TextHashTestEntry(test_string="vb", expected_int=5798561, expected_str="0x587AA1", hash_size=4),
        TextHashTestEntry(test_string="boneremap", expected_int=255353250, expected_str="0xF3861A2", hash_size=4),
    ]

    for hash_entry in hash_data_list:
        # check expected result from first execution
        test_result = rx3_handler.calculate_rx3_hash_from_string(hash_entry.test_string, hash_size=hash_entry.hash_size if hash_entry.hash_size else 8)
        test_result_str = convert_int_to_hex_string(test_result)
        assert test_result == hash_entry.expected_int
        assert test_result_str == hash_entry.expected_str

        # check if result is the same after second execution
        test_result = rx3_handler.calculate_rx3_hash_from_string(hash_entry.test_string, hash_size=hash_entry.hash_size if hash_entry.hash_size else 8)
        test_result_str = convert_int_to_hex_string(test_result)
        assert test_result == hash_entry.expected_int
        assert test_result_str == hash_entry.expected_str


@pytest.mark.unittest
def test_hash_rx3_from_bytes_to_match_expected_result():
    hash_data_list = [
        BytesHashTestEntry(test_bytes=b"texturebatch", expected_int=1808827868, expected_str="0x6BD085DC", hash_size=4),
        BytesHashTestEntry(test_bytes=b"texture", expected_int=2047566042, expected_str="0x7A0B60DA", hash_size=4),
        BytesHashTestEntry(test_bytes=b"ib", expected_int=5798132, expected_str="0x5878F4", hash_size=4),
        BytesHashTestEntry(test_bytes=b"vb", expected_int=5798561, expected_str="0x587AA1", hash_size=4),
        BytesHashTestEntry(test_bytes=b"boneremap", expected_int=255353250, expected_str="0xF3861A2", hash_size=4),
    ]

    for hash_entry in hash_data_list:
        # check expected result from first execution
        test_result = rx3_handler.calculate_rx3_hash_from_bytes(hash_entry.test_bytes, hash_size=hash_entry.hash_size if hash_entry.hash_size else 8)
        test_result_str = convert_int_to_hex_string(test_result)
        assert test_result == hash_entry.expected_int
        assert test_result_str == hash_entry.expected_str

        # check if result is the same after second execution
        test_result = rx3_handler.calculate_rx3_hash_from_bytes(hash_entry.test_bytes, hash_size=hash_entry.hash_size if hash_entry.hash_size else 8)
        test_result_str = convert_int_to_hex_string(test_result)
        assert test_result == hash_entry.expected_int
        assert test_result_str == hash_entry.expected_str
