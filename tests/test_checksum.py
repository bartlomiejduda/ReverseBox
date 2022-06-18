import zlib
import pytest
from faker import Faker
from checksum.checksum_handler import ChecksumHandler

checksum_handler = ChecksumHandler()
fake = Faker()


@pytest.mark.unittest
def test_checksum_calculate_crc32_to_match_zlib_result():

    test_data_array = [b'123456789', b'Hello Python', b'Secret123@123#!', b'\x00\x01\x02\x03', b'1', b'abcdefgh',
                       fake.binary(length=100), fake.binary(length=5000)]

    for test_data in test_data_array:
        test_result = checksum_handler.calculate_crc32(test_data)
        zlib_result = zlib.crc32(test_data)
        zlib_result_str = "0x%02X" % int(zlib_result)
        test_result_str = "0x%02X" % int(test_result)
        assert test_result == zlib_result
        assert zlib_result_str == test_result_str


@pytest.mark.unittest
def test_checksum_calculate_crc32_to_match_expected_result():
    test_data = b'123456789'
    expected_result = 3421780262
    expected_result_str = "0xCBF43926"

    # check expected result from first execution
    test_result = checksum_handler.calculate_crc32(test_data)
    test_result_str = "0x%02X" % int(test_result)
    assert test_result == expected_result
    assert test_result_str == expected_result_str

    # check if result is the same after second execution
    test_result = checksum_handler.calculate_crc32(test_data)
    test_result_str = "0x%02X" % int(test_result)
    assert test_result == expected_result
    assert test_result_str == expected_result_str
