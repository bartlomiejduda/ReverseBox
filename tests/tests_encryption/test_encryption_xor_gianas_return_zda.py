"""
Copyright © 2023  Bartłomiej Duda
License: GPL-3.0 License
"""

# fmt: off

import pytest

from reversebox.encryption.encryption_xor_gianas_return_zda import (
    xor_zda_decrypt_data,
    xor_zda_encrypt_data,
)
from tests.common import XORTestEntry


@pytest.mark.unittest
def test_encryption_xor_gianas_return_zda_to_match_expected_result():
    xor_data_list = [
        XORTestEntry(test_data=b"abcd", key=b"", expected_result=b"\xDA\x03\x01\x07"),
        XORTestEntry(test_data=b"BM", key=b"", expected_result=b"\xF9\x0F"),
    ]

    for test_entry in xor_data_list:
        encrypted_test_result = xor_zda_encrypt_data(test_entry.test_data)
        assert encrypted_test_result == test_entry.expected_result

        decrypted_test_result = xor_zda_decrypt_data(encrypted_test_result)
        assert decrypted_test_result == test_entry.test_data


# fmt: on
