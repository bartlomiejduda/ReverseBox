"""
Copyright © 2024-2025  Bartłomiej Duda
License: GPL-3.0 License
"""

import pytest

from reversebox.common.common import convert_int_to_hex_string
from reversebox.hash.hash_djb2 import DJB2Handler
from tests.common import BytesHashTestEntry, TextHashTestEntry

djb2_handler = DJB2Handler()


# fmt: off

@pytest.mark.unittest
def test_hash_djb2_from_string_to_match_expected_result():
    hash_data_list = [
        TextHashTestEntry(
            test_string="data/xenon/loc/eng/database/eng_us-meta.xml", expected_int=15231288347764836083, expected_str="0xD360680DB011C6F3"
        ),
        TextHashTestEntry(
            test_string="data/xenon/gameexplorer/common/textures/watermark_right.xpr", expected_int=7560285221075454525, expected_str="0x68EB875A3AD68A3D"
        ),
        TextHashTestEntry(
            test_string="data/common/config/videoheap.cfg", expected_int=5848927340003809502, expected_str="0x512B906D41FF58DE"
        ),
        TextHashTestEntry(test_string="Hello", expected_int=210676686969, expected_str="0x310D4F2079"),  # https://theartincode.stanis.me/008-djb2/
        TextHashTestEntry(test_string="Hello!", expected_int=6952330670010, expected_str="0x652B7332FBA"),
        TextHashTestEntry(test_string="abcd", expected_int=6385036879, expected_str="0x17C93EE4F"),
        TextHashTestEntry(test_string="123456789", expected_int=249811310476114818, expected_str="0x377821035CDBB82"),
        TextHashTestEntry(test_string="123", expected_int=193432059, expected_str="0xB8789FB"),
        TextHashTestEntry(test_string="Secret123@123", expected_int=5791429533929400023, expected_str="0x505F4A7A0F9166D7"),
        TextHashTestEntry(test_string="", expected_int=5381, expected_str="0x1505"),
        TextHashTestEntry(test_string=" ", expected_int=177605, expected_str="0x2B5C5"),
        TextHashTestEntry(test_string="i/IMG_GRADE_12", expected_int=580088926, expected_str="0x2293745E", hash_size=4),  # Room of Prey 3 (Android)
        TextHashTestEntry(test_string="t/T_SYS", expected_int=1491806618, expected_str="0x58EB299A", hash_size=4),  # Room of Prey 3 (Android)
        TextHashTestEntry(test_string="snd/S_EFF_28.ogg", expected_int=178497392, expected_str="0xAA3A770", hash_size=4),  # Room of Prey 3 (Android)
    ]

    for hash_entry in hash_data_list:
        # check expected result from first execution
        test_result = djb2_handler.calculate_djb2_hash_from_string(hash_entry.test_string, hash_size=hash_entry.hash_size if hash_entry.hash_size else 8)
        test_result_str = convert_int_to_hex_string(test_result)
        assert test_result == hash_entry.expected_int
        assert test_result_str == hash_entry.expected_str

        # check if result is the same after second execution
        test_result = djb2_handler.calculate_djb2_hash_from_string(hash_entry.test_string, hash_size=hash_entry.hash_size if hash_entry.hash_size else 8)
        test_result_str = convert_int_to_hex_string(test_result)
        assert test_result == hash_entry.expected_int
        assert test_result_str == hash_entry.expected_str


@pytest.mark.unittest
def test_hash_djb2_from_bytes_to_match_expected_result():
    hash_data_list = [
        BytesHashTestEntry(
            test_bytes=b"data/xenon/loc/eng/database/eng_us-meta.xml", expected_int=15231288347764836083, expected_str="0xD360680DB011C6F3"
        ),
        BytesHashTestEntry(
            test_bytes=b"data/xenon/gameexplorer/common/textures/watermark_right.xpr", expected_int=7560285221075454525, expected_str="0x68EB875A3AD68A3D"
        ),
        BytesHashTestEntry(
            test_bytes=b"data/common/config/videoheap.cfg", expected_int=5848927340003809502, expected_str="0x512B906D41FF58DE"
        ),
        BytesHashTestEntry(test_bytes=b"Hello", expected_int=210676686969, expected_str="0x310D4F2079"),  # https://theartincode.stanis.me/008-djb2/
        BytesHashTestEntry(test_bytes=b"Hello!", expected_int=6952330670010, expected_str="0x652B7332FBA"),
        BytesHashTestEntry(test_bytes=b"abcd", expected_int=6385036879, expected_str="0x17C93EE4F"),
        BytesHashTestEntry(test_bytes=b"123456789", expected_int=249811310476114818, expected_str="0x377821035CDBB82"),
        BytesHashTestEntry(test_bytes=b"123", expected_int=193432059, expected_str="0xB8789FB"),
        BytesHashTestEntry(test_bytes=b"Secret123@123", expected_int=5791429533929400023, expected_str="0x505F4A7A0F9166D7"),
        BytesHashTestEntry(test_bytes=b"", expected_int=5381, expected_str="0x1505"),
        BytesHashTestEntry(test_bytes=b" ", expected_int=177605, expected_str="0x2B5C5"),
        BytesHashTestEntry(test_bytes=b"i/IMG_GRADE_12", expected_int=580088926, expected_str="0x2293745E", hash_size=4),  # Room of Prey 3 (Android)
        BytesHashTestEntry(test_bytes=b"t/T_SYS", expected_int=1491806618, expected_str="0x58EB299A", hash_size=4),  # Room of Prey 3 (Android)
        BytesHashTestEntry(test_bytes=b"snd/S_EFF_28.ogg", expected_int=178497392, expected_str="0xAA3A770", hash_size=4),  # Room of Prey 3 (Android)
    ]

    for hash_entry in hash_data_list:
        # check expected result from first execution
        test_result = djb2_handler.calculate_djb2_hash_from_bytes(hash_entry.test_bytes, hash_size=hash_entry.hash_size if hash_entry.hash_size else 8)
        test_result_str = convert_int_to_hex_string(test_result)
        assert test_result == hash_entry.expected_int
        assert test_result_str == hash_entry.expected_str

        # check if result is the same after second execution
        test_result = djb2_handler.calculate_djb2_hash_from_bytes(hash_entry.test_bytes, hash_size=hash_entry.hash_size if hash_entry.hash_size else 8)
        test_result_str = convert_int_to_hex_string(test_result)
        assert test_result == hash_entry.expected_int
        assert test_result_str == hash_entry.expected_str
