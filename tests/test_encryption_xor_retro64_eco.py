import pytest
from common import XORRetro64ECOTestEntry
from reversebox.encryption.encryption_xor_retro64_eco import xor_cipher_retro64_eco

# Tests for XOR Cipher used in Retro64 *.ECO files
# Read more here: http://wiki.xentax.com/index.php/Retro64_ECO


@pytest.mark.unittest
def test_encryption_xor_retro64_to_match_expected_result():
    xor_data_list = [
        XORRetro64ECOTestEntry(test_data=b'abcd', key=49152, expected_result=b'\x18\xFC\x5C\xEF'),
        XORRetro64ECOTestEntry(test_data=b'aaaa', key=49152, expected_result=b'\x18\xFF\x5E\xEA'),
                     ]

    for test_entry in xor_data_list:
        encrypted_test_result = xor_cipher_retro64_eco(test_entry.test_data, test_entry.key)
        assert encrypted_test_result == test_entry.expected_result

        decrypted_test_result = xor_cipher_retro64_eco(encrypted_test_result, test_entry.key)
        assert decrypted_test_result == test_entry.test_data


