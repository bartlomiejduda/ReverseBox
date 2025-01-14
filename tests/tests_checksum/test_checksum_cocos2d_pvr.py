"""
Copyright © 2025  Bartłomiej Duda
License: GPL-3.0 License
"""

import os

import pytest

from reversebox.checksum.checksum_cocos2d_pvr import Cocos2dPVRChecksumHandler
from reversebox.io_files.file_handler import FileHandler

cocos2d_pvr_checksum_handler = Cocos2dPVRChecksumHandler()

# fmt: off


@pytest.mark.unittest
def test_checksum_calculate_cocos2d_pcr_checksum_to_match_expected_result():

    # read from encrypted file
    cocos2d_file_path = os.path.join(os.path.dirname(__file__), "checksum_files/cg001_i01.png")
    cocos2d_file = FileHandler(cocos2d_file_path, "rb")
    cocos2d_file.seek(8)
    cocos2d_file.change_endianess("big")
    f_checksum: int = cocos2d_file.read_uint32()
    f_size: int = cocos2d_file.get_file_size()
    checksum_data_size: int = (f_size - 12) // 4
    cocos2d_file.close()

    # read from decrypted file
    cocos2d_decrypted_file_path = os.path.join(os.path.dirname(__file__), "checksum_files/cg001_i01_decrypted.png")
    cocos2d_decrypted_file = FileHandler(cocos2d_decrypted_file_path, "rb")
    cocos2d_decrypted_file.seek(12)
    read_data_size: int = f_size - 12
    decrypted_data: bytes = cocos2d_decrypted_file.read_bytes(read_data_size)
    cocos2d_decrypted_file.close()

    # calculate checksum
    calculated_checksum: int = cocos2d_pvr_checksum_handler.calculate_cocos2d_pvr_checksum(decrypted_data, checksum_data_size)
    assert calculated_checksum == f_checksum
