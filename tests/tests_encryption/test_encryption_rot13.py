"""
Copyright © 2023  Bartłomiej Duda
License: GPL-3.0 License
"""

import pytest

from reversebox.encryption.encryption_rot13 import (
    rot13_cipher_decrypt,
    rot13_cipher_encrypt,
)
from tests.common import ROT13TestEntry


@pytest.mark.unittest
def test_encryption_rot13_to_match_expected_result():
    rot_data_list = [
        ROT13TestEntry(
            test_data=b"\x01\x02\x03", key=b"abc", expected_result=b"\x62\x64\x66"
        ),
        ROT13TestEntry(
            test_data=b"abcd",
            key=b"abc",
            expected_result=b"\xC2\xC4\xC6\xC5",
        ),
        ROT13TestEntry(
            test_data=b"Secret123#123",
            key=b"\xAA\xAA\xAA\xAA\xBB\xBB",
            expected_result=b"\xFD\x0F\x0D\x1C\x20\x2F\xDB\xDC\xDD\xCD\xEC\xED\xDD",
        ),
    ]

    for test_entry in rot_data_list:
        encrypted_test_result = rot13_cipher_encrypt(
            test_entry.test_data, test_entry.key
        )
        assert encrypted_test_result == test_entry.expected_result

        decrypted_test_result = rot13_cipher_decrypt(
            encrypted_test_result, test_entry.key
        )
        assert decrypted_test_result == test_entry.test_data
