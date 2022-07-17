import pytest
from tests.common import XORRetro64ECOTestEntry
from reversebox.encryption.encryption_xor_retro64_eco import xor_cipher_retro64_eco

# Tests for XOR Cipher used in Retro64 *.ECO files
# Read more here: http://wiki.xentax.com/index.php/Retro64_ECO


@pytest.mark.unittest
def test_encryption_xor_retro64_to_match_expected_result():
    xor_data_list = [
        XORRetro64ECOTestEntry(test_data=b'abcd', key=49152, expected_result=b'\x18\xFC\x5C\xEF'),
        XORRetro64ECOTestEntry(test_data=b'aaaa', key=49152, expected_result=b'\x18\xFF\x5E\xEA'),
        XORRetro64ECOTestEntry(test_data=b'abcd', key=13, expected_result=b'\x2B\x05\xA7\xD5'),
        XORRetro64ECOTestEntry(test_data=b'aaaa', key=13, expected_result=b'\x2B\x06\xA5\xD0'),
        XORRetro64ECOTestEntry(test_data=b'ABCDEFGH', key=8000, expected_result=b'\xC4\xA5\xBA\xDE\x62\x44\x8E\xB6'),
        XORRetro64ECOTestEntry(test_data=b'ABCD', key=0, expected_result=b'\x4A\xF4\x44\x8A'),
        XORRetro64ECOTestEntry(test_data=b'ABCD', key=1, expected_result=b'\x95\xE4\x41\x88'),
        XORRetro64ECOTestEntry(test_data=b'!@#$%', key=1234, expected_result=b'\x1C\x19\xC9\xAA\xB0'),
        XORRetro64ECOTestEntry(test_data=b'', key=1234, expected_result=b''),
        XORRetro64ECOTestEntry(test_data=b'', key=436346, expected_result=b''),
        XORRetro64ECOTestEntry(test_data=b'abcd', key=99999999999, expected_result=b'\x34\x5B\xA9\xA2'),
                     ]

    for test_entry in xor_data_list:
        encrypted_test_result = xor_cipher_retro64_eco(test_entry.test_data, test_entry.key)
        assert encrypted_test_result == test_entry.expected_result

        decrypted_test_result = xor_cipher_retro64_eco(encrypted_test_result, test_entry.key)
        assert decrypted_test_result == test_entry.test_data


