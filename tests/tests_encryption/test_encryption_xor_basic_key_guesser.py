"""
Copyright © 2024  Bartłomiej Duda
License: GPL-3.0 License
"""

import pytest

from reversebox.encryption.encryption_xor_basic_key_guesser import xor_basic_guess_key
from tests.common import XORGuesserEntry


# fmt: off
@pytest.mark.unittest
def test_encryption_xor_basic_guesser_to_match_expected_xor_key_to_be_found():
    xor_data_list = [
        XORGuesserEntry(encrypted_data=b"\x78\x23", decrypted_data=b"\x38\x63", max_key_length=2, expected_xor_key=b"\x40"),
        XORGuesserEntry(encrypted_data=b"\x2A\x13\x07\x37", decrypted_data=b"\x4C\x75\x61\x51", max_key_length=2, expected_xor_key=b"\x66"),  # LuaQ file
    ]

    for test_entry in xor_data_list:
        found_xor_key = xor_basic_guess_key(test_entry.encrypted_data, test_entry.decrypted_data, test_entry.max_key_length)
        assert found_xor_key == test_entry.expected_xor_key
# fmt: on
