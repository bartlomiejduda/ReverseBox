import zlib
import pytest
from faker import Faker
from reversebox.checksum.checksum_crc32 import CRC32Handler
from reversebox.common.common import convert_int_to_hex_string

crc32_handler = CRC32Handler()
fake = Faker()


@pytest.mark.unittest
def test_checksum_calculate_crc32_to_match_zlib_result():

    test_data_array = [b'', b'123456789', b'Hello Python', b'Secret123@123#!', b'\x00\x01\x02\x03', b'1', b'abcdefgh',
                       b'\n', b'!@#$%^&*()', fake.binary(length=100), fake.binary(length=5000)]

    for test_data in test_data_array:
        test_result = crc32_handler.calculate_crc32(test_data)
        zlib_result = zlib.crc32(test_data)
        test_result_str = convert_int_to_hex_string(test_result)
        zlib_result_str = convert_int_to_hex_string(zlib_result)
        assert test_result == zlib_result
        assert test_result_str == zlib_result_str


@pytest.mark.unittest
def test_checksum_calculate_crc32_to_match_expected_result():
    test_data = b'123456789'
    expected_result = 3421780262
    expected_result_str = "0xCBF43926"

    # check expected result from first execution
    test_result = crc32_handler.calculate_crc32(test_data)
    test_result_str = convert_int_to_hex_string(test_result)
    assert test_result == expected_result
    assert test_result_str == expected_result_str

    # check if result is the same after second execution
    test_result = crc32_handler.calculate_crc32(test_data)
    test_result_str = convert_int_to_hex_string(test_result)
    assert test_result == expected_result
    assert test_result_str == expected_result_str
