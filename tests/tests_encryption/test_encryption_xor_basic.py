"""
Copyright © 2022-2024  Bartłomiej Duda
License: GPL-3.0 License
"""

import pytest

from reversebox.encryption.encryption_xor_basic import xor_cipher_basic
from tests.common import XORTestEntry


# fmt: off
@pytest.mark.unittest
def test_encryption_xor_basic_to_match_expected_result():
    xor_data_list = [
        XORTestEntry(test_data=b"abcd", key=b"\x3D", expected_result=b"\x5C\x5F\x5E\x59"),
        XORTestEntry(test_data=b"aaaa", key=b"\xAA\xAA\xAA\xAA", expected_result=b"\xCB\xCB\xCB\xCB"),
        XORTestEntry(test_data=b"aaaa", key=b"\xAA\xAA\xAA\xAA\xBB\xBB", expected_result=b"\xCB\xCB\xCB\xCB"),
        XORTestEntry(test_data=b"aaaa", key=b"\xAA", expected_result=b"\xCB\xCB\xCB\xCB"),
        XORTestEntry(test_data=b"aaaa", key=b"aaaa", expected_result=b"\x00\x00\x00\x00"),
        XORTestEntry(test_data=b"", key=b"", expected_result=b""),
        XORTestEntry(test_data=b"", key=b"aaaa", expected_result=b""),
        XORTestEntry(test_data=b"aaaa", key=b"", expected_result=b"aaaa"),
        XORTestEntry(test_data=b"\x01\x02\x03\x04", key=b"\x3D", expected_result=b"\x3C\x3F\x3E\x39"),
        XORTestEntry(test_data=b"\x01\x02\x03\x04", key=b"\xAA\xAA\xAA\xAA", expected_result=b"\xAB\xA8\xA9\xAE"),
        XORTestEntry(test_data=b"\x01\x02\x03\x04", key=b"\xAA\xAA\xAA\xAA\xCC\xCC", expected_result=b"\xAB\xA8\xA9\xAE"),
        XORTestEntry(test_data=b"\x01\x02\x03\x04", key=b"\xAA", expected_result=b"\xAB\xA8\xA9\xAE"),
        XORTestEntry(test_data=b"\x00\x00\x00\x00", key=b"\xFF\xFF\xFF\xFF", expected_result=b"\xFF\xFF\xFF\xFF"),
        XORTestEntry(test_data=b"Secret123#123", key=b"\xB5\xC8", expected_result=b"\xE6\xAD\xD6\xBA\xD0\xBC\x84\xFA\x86\xEB\x84\xFA\x86"),
        XORTestEntry(test_data=b"ABCDEFGH", key=b"\xB5\xC8", expected_result=b"\xF4\x8A\xF6\x8C\xF0\x8E\xF2\x80"),
        XORTestEntry(test_data=b"!@#$%^&*()", key=b"\xB5\xC8", expected_result=b"\x94\x88\x96\xEC\x90\x96\x93\xE2\x9D\xE1"),
        XORTestEntry(test_data=b"oneseek", key=b"P", expected_result=b"?>5#55;"),
        XORTestEntry(test_data=b"hello", key=b"101ComputingKey", expected_result=b"YU]/\x00"),
        XORTestEntry(test_data=b"abcd", key=b"101ComputingKey", expected_result=b"PRR'"),
        XORTestEntry(test_data=b"python", key=b"101ComputingKey", expected_result=b"AIE+\x00\x03"),
        XORTestEntry(test_data=b"dog", key=b"101ComputingKey", expected_result=b"U_V"),
        XORTestEntry(test_data=b"Wiki", key=b"\xF3", expected_result=b"\xA4\x9A\x98\x9A"),
        XORTestEntry(test_data=b"secret", key=b"key", expected_result=b"\x18\x00\x1a\x19\x00\r"),
        XORTestEntry(test_data=b"Secret123#123", key=b"Very#Strong567342Key", expected_result=b"\x05\x00\x11\x0bF'E@\\MV\x07\x05"),
        XORTestEntry(test_data=b"XorSecretData", key=b"XorKey", expected_result=b"\x00\x00\x00\x18\x00\x1a*\n\x06\x0f\x04\r9"),
        XORTestEntry(test_data=b"AAAAbbbbCCCC1111dddd", key=b"key", expected_result=b"*$8*\x07\x1b\t\x07:(&:ZTHZ\x01\x1d\x0f\x01"),
        XORTestEntry(test_data=b"a", key=b"a", expected_result=b"\x00"),
        XORTestEntry(test_data=b"secret", key=b"secret", expected_result=b"\x00\x00\x00\x00\x00\x00"),
        XORTestEntry(test_data=b"python", key=b"python", expected_result=b"\x00\x00\x00\x00\x00\x00"),
        XORTestEntry(test_data=b"\x2A\x13\x07\x37", key=b"\x66", expected_result=b"LuaQ"),
    ]

    for test_entry in xor_data_list:
        encrypted_test_result = xor_cipher_basic(test_entry.test_data, test_entry.key)
        assert encrypted_test_result == test_entry.expected_result

        decrypted_test_result = xor_cipher_basic(encrypted_test_result, test_entry.key)
        assert decrypted_test_result == test_entry.test_data
