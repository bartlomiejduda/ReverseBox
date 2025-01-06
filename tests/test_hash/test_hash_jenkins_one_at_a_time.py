"""
Copyright © 2025  Bartłomiej Duda
License: GPL-3.0 License
"""

import pytest

from reversebox.common.common import convert_int_to_hex_string
from reversebox.hash.hash_jenkins_one_at_a_time import JenkinsOneAtATimeHandler
from tests.common import BytesHashTestEntry, TextHashTestEntry

jenkins_one_at_a_time_handler = JenkinsOneAtATimeHandler()


# fmt: off

@pytest.mark.unittest
def test_hash_jenkins_one_at_a_time_from_string_to_match_expected_result():
    hash_data_list = [
        # Examples from https://en.wikipedia.org/wiki/Jenkins_hash_function
        TextHashTestEntry(test_string="a", expected_int=3392050242, expected_str="0xCA2E9442"),
        TextHashTestEntry(test_string="The quick brown fox jumps over the lazy dog", expected_int=1369346549, expected_str="0x519E91F5"),
    ]

    for hash_entry in hash_data_list:
        # check expected result from first execution
        test_result = jenkins_one_at_a_time_handler.calculate_jenkins_one_at_a_time_hash_from_string(hash_entry.test_string)
        test_result_str = convert_int_to_hex_string(test_result)
        assert test_result == hash_entry.expected_int
        assert test_result_str == hash_entry.expected_str

        # check if result is the same after second execution
        test_result = jenkins_one_at_a_time_handler.calculate_jenkins_one_at_a_time_hash_from_string(hash_entry.test_string)
        test_result_str = convert_int_to_hex_string(test_result)
        assert test_result == hash_entry.expected_int
        assert test_result_str == hash_entry.expected_str


@pytest.mark.unittest
def test_hash_jenkins_one_at_a_time_from_bytes_to_match_expected_result():
    hash_data_list = [
        # Examples from https://en.wikipedia.org/wiki/Jenkins_hash_function
        BytesHashTestEntry(test_bytes=b"a", expected_int=3392050242, expected_str="0xCA2E9442"),
        BytesHashTestEntry(test_bytes=b"The quick brown fox jumps over the lazy dog", expected_int=1369346549, expected_str="0x519E91F5"),
    ]

    for hash_entry in hash_data_list:
        # check expected result from first execution
        test_result = jenkins_one_at_a_time_handler.calculate_jenkins_one_at_a_time_hash_from_bytes(hash_entry.test_bytes)
        test_result_str = convert_int_to_hex_string(test_result)
        assert test_result == hash_entry.expected_int
        assert test_result_str == hash_entry.expected_str

        # check if result is the same after second execution
        test_result = jenkins_one_at_a_time_handler.calculate_jenkins_one_at_a_time_hash_from_bytes(hash_entry.test_bytes)
        test_result_str = convert_int_to_hex_string(test_result)
        assert test_result == hash_entry.expected_int
        assert test_result_str == hash_entry.expected_str
