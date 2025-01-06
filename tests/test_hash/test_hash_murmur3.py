"""
Copyright © 2025  Bartłomiej Duda
License: GPL-3.0 License
"""

import pytest

from reversebox.common.common import convert_int_to_hex_string
from reversebox.hash.hash_murmur3 import Murmur3Handler
from tests.common import BytesHashTestEntry, TextHashTestEntry

murmur3_handler = Murmur3Handler()


# fmt: off

@pytest.mark.unittest
def test_hash_murmur3_from_string_to_match_expected_result():
    hash_data_list = [
        # Examples from https://en.wikipedia.org/wiki/MurmurHash#Algorithm
        TextHashTestEntry(test_string="", expected_int=0, expected_str="0x00", seed=0x00000000),
        TextHashTestEntry(test_string="", expected_int=1364076727, expected_str="0x514E28B7", seed=0x00000001),
        TextHashTestEntry(test_string="", expected_int=2180083513, expected_str="0x81F16F39", seed=0xffffffff),
        TextHashTestEntry(test_string="test", expected_int=3127628307, expected_str="0xBA6BD213", seed=0x00000000),
        TextHashTestEntry(test_string="test", expected_int=1883996636, expected_str="0x704B81DC", seed=0x9747b28c),
        TextHashTestEntry(test_string="Hello, world!", expected_int=3224780355, expected_str="0xC0363E43", seed=0x00000000),
        TextHashTestEntry(test_string="Hello, world!", expected_int=612912314, expected_str="0x24884CBA", seed=0x9747b28c),
        TextHashTestEntry(test_string="The quick brown fox jumps over the lazy dog", expected_int=776992547, expected_str="0x2E4FF723", seed=0x00000000),
        TextHashTestEntry(test_string="The quick brown fox jumps over the lazy dog", expected_int=799549133, expected_str="0x2FA826CD", seed=0x9747b28c),
    ]

    for hash_entry in hash_data_list:
        # check expected result from first execution
        test_result = murmur3_handler.calculate_murmur3_hash_from_string(hash_entry.test_string, seed=hash_entry.seed)
        test_result_str = convert_int_to_hex_string(test_result)
        assert test_result == hash_entry.expected_int
        assert test_result_str == hash_entry.expected_str

        # check if result is the same after second execution
        test_result = murmur3_handler.calculate_murmur3_hash_from_string(hash_entry.test_string, seed=hash_entry.seed)
        test_result_str = convert_int_to_hex_string(test_result)
        assert test_result == hash_entry.expected_int
        assert test_result_str == hash_entry.expected_str


@pytest.mark.unittest
def test_hash_murmur3_from_bytes_to_match_expected_result():
    hash_data_list = [
        # Examples from https://en.wikipedia.org/wiki/MurmurHash#Algorithm
        BytesHashTestEntry(test_bytes=b"", expected_int=0, expected_str="0x00", seed=0x00000000),
        BytesHashTestEntry(test_bytes=b"", expected_int=1364076727, expected_str="0x514E28B7", seed=0x00000001),
        BytesHashTestEntry(test_bytes=b"", expected_int=2180083513, expected_str="0x81F16F39", seed=0xffffffff),
        BytesHashTestEntry(test_bytes=b"test", expected_int=3127628307, expected_str="0xBA6BD213", seed=0x00000000),
        BytesHashTestEntry(test_bytes=b"test", expected_int=1883996636, expected_str="0x704B81DC", seed=0x9747b28c),
        BytesHashTestEntry(test_bytes=b"Hello, world!", expected_int=3224780355, expected_str="0xC0363E43", seed=0x00000000),
        BytesHashTestEntry(test_bytes=b"Hello, world!", expected_int=612912314, expected_str="0x24884CBA", seed=0x9747b28c),
        BytesHashTestEntry(test_bytes=b"The quick brown fox jumps over the lazy dog", expected_int=776992547, expected_str="0x2E4FF723", seed=0x00000000),
        BytesHashTestEntry(test_bytes=b"The quick brown fox jumps over the lazy dog", expected_int=799549133, expected_str="0x2FA826CD", seed=0x9747b28c),
    ]

    for hash_entry in hash_data_list:
        # check expected result from first execution
        test_result = murmur3_handler.calculate_murmur3_hash_from_bytes(hash_entry.test_bytes, seed=hash_entry.seed)
        test_result_str = convert_int_to_hex_string(test_result)
        assert test_result == hash_entry.expected_int
        assert test_result_str == hash_entry.expected_str

        # check if result is the same after second execution
        test_result = murmur3_handler.calculate_murmur3_hash_from_bytes(hash_entry.test_bytes, seed=hash_entry.seed)
        test_result_str = convert_int_to_hex_string(test_result)
        assert test_result == hash_entry.expected_int
        assert test_result_str == hash_entry.expected_str
