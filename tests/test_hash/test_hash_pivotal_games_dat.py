"""
Copyright © 2025  Bartłomiej Duda
License: GPL-3.0 License
"""

import pytest

from reversebox.common.common import convert_int_to_hex_string
from reversebox.hash.hash_pivotal_games_dat import PivotalGamesDATHashHandler
from tests.common import TextHashTestEntry

hash_handler = PivotalGamesDATHashHandler()


# fmt: off

@pytest.mark.unittest
def test_hash_pivotal_games_dat_from_string_to_match_expected_result():
    hash_data_list = [
        TextHashTestEntry(test_string="MPD_UH1_HUEY_TAILROTOR.DDS", expected_int=2038369709, expected_str="0x797F0DAD"),
        TextHashTestEntry(test_string="mpd_usglasses.dds", expected_int=3525764600, expected_str="0xD226E5F8"),
        TextHashTestEntry(test_string="MPD_USGLASSES.DDS", expected_int=3544284667, expected_str="0xD3417DFB"),
        TextHashTestEntry(test_string="mpd_usglasses.evo", expected_int=3539855468, expected_str="0xD2FDE86C"),
        TextHashTestEntry(test_string="MPD_USWEBBING_03_COMPASSPOUCH_WET.DDS", expected_int=2189375299, expected_str="0x827F3743"),
        TextHashTestEntry(test_string="MPD_US_101_DEAD_01.EVO", expected_int=431098015, expected_str="0x19B2089F"),
        TextHashTestEntry(test_string="mpd_us_101_dead_02.evo", expected_int=1073481072, expected_str="0x3FFC0570"),
    ]

    for hash_entry in hash_data_list:
        # check expected result from first execution
        test_result = hash_handler.calculate_pivotal_games_dat_hash_from_string(hash_entry.test_string)
        test_result_str = convert_int_to_hex_string(test_result)
        assert test_result == hash_entry.expected_int
        assert test_result_str == hash_entry.expected_str

        # check if result is the same after second execution
        test_result = hash_handler.calculate_pivotal_games_dat_hash_from_string(hash_entry.test_string)
        test_result_str = convert_int_to_hex_string(test_result)
        assert test_result == hash_entry.expected_int
        assert test_result_str == hash_entry.expected_str
