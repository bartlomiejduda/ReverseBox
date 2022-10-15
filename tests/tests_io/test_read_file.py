"""
Copyright © 2022  Bartłomiej Duda
License: GPL-3.0 License
"""
import os

import pytest

from reversebox.io_files.file_handler import FileHandler


@pytest.mark.unittest
def test_open_seek_and_read_little_endian_file():
    file_path = os.path.join(os.path.dirname(__file__), "data\\fake_file3_le.bin")

    file_reader = FileHandler(file_path, "rb")
    file_reader.open()

    value1 = file_reader.read_str(4, "utf8")
    assert value1 == "ABCD"

    value2 = file_reader.read_uint32()
    assert value2 == 100

    value3 = file_reader.read_uint16()
    assert value3 == 101

    value4 = file_reader.read_uint8()
    assert value4 == 102

    file_reader.seek(4)
    value5 = file_reader.read_uint32()
    assert value5 == 100

    result = file_reader.close()
    assert result


@pytest.mark.unittest
def test_open_seek_and_read_big_endian_file():
    file_path = os.path.join(os.path.dirname(__file__), "data\\fake_file4_be.bin")

    file_reader = FileHandler(file_path, "rb", "big")
    file_reader.open()

    value1 = file_reader.read_str(4, "utf8")
    assert value1 == "DCBA"

    value2 = file_reader.read_uint32()
    assert value2 == 100

    value3 = file_reader.read_uint16()
    assert value3 == 101

    value4 = file_reader.read_uint8()
    assert value4 == 102

    file_reader.seek(4)
    value5 = file_reader.read_uint32()
    assert value5 == 100

    result = file_reader.close()
    assert result


@pytest.mark.unittest
def test_open_and_read_multi_endian_file():
    file_path = os.path.join(
        os.path.dirname(__file__), "data\\fake_file5_multi_endian.bin"
    )

    file_reader = FileHandler(file_path, "rb", "little")
    file_reader.open()

    value1 = file_reader.read_str(4, "utf8")
    assert value1 == "AAAA"

    value2 = file_reader.read_uint32()
    assert value2 == 100

    value3 = file_reader.read_uint16()
    assert value3 == 101

    value4 = file_reader.read_uint8()
    assert value4 == 102

    file_reader.change_endianess("big")

    value5 = file_reader.read_str(4, "utf8")
    assert value5 == "BBBB"

    value6 = file_reader.read_uint32()
    assert value6 == 100

    value7 = file_reader.read_uint16()
    assert value7 == 101

    value8 = file_reader.read_uint8()
    assert value8 == 102

    result = file_reader.close()
    assert result
