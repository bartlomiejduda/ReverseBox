"""
Copyright © 2022  Bartłomiej Duda
License: GPL-3.0 License
"""
import os

import pytest

from reversebox.io_files.file_handler import FileHandler


@pytest.mark.unittest
def test_open_and_write_little_endian_file():
    file_path = os.path.join(os.path.dirname(__file__), "data\\fake_file6_le.bin")

    file_handler = FileHandler(file_path, "wb")
    file_handler.open()

    result = file_handler.write_str("WB01")
    assert result
    result = file_handler.write_uint32(100)
    assert result
    result = file_handler.write_uint16(101)
    assert result
    result = file_handler.write_uint8(102)
    assert result
    result = file_handler.write_bytes(b"\x41\x42\x43\x44")
    assert result

    result = file_handler.close()
    assert result
