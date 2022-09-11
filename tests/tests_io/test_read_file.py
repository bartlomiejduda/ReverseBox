"""
Copyright © 2022  Bartłomiej Duda
License: GPL-3.0 License
"""
import os

import pytest

from reversebox.io_files.file_reader import FileReader


@pytest.mark.unittest
def test_open_seek_and_read_little_endian_file():
    file_path = os.path.join(os.path.dirname(__file__), "data\\fake_file3_le.bin")

    file_reader = FileReader(file_path, "rb")
    file_reader.open()

    value1 = file_reader.read_str(4, "utf8")
    assert value1 == "ABCD"

    value2 = file_reader.read_uint32_le()
    assert value2 == 100

    value3 = file_reader.read_uint16_le()
    assert value3 == 101

    value4 = file_reader.read_uint8()
    assert value4 == 102

    file_reader.seek(4)
    value5 = file_reader.read_uint32_le()
    assert value5 == 100

    result = file_reader.close()
    assert result


@pytest.mark.unittest
def test_open_seek_and_read_big_endian_file():
    file_path = os.path.join(os.path.dirname(__file__), "data\\fake_file4_be.bin")

    file_reader = FileReader(file_path, "rb")
    file_reader.open()

    value1 = file_reader.read_str(4, "utf8")
    assert value1 == "DCBA"

    value2 = file_reader.read_uint32_be()
    assert value2 == 100

    value3 = file_reader.read_uint16_be()
    assert value3 == 101

    value4 = file_reader.read_uint8()
    assert value4 == 102

    file_reader.seek(4)
    value5 = file_reader.read_uint32_be()
    assert value5 == 100

    result = file_reader.close()
    assert result
