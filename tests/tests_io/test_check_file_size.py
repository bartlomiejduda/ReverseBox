"""
Copyright © 2022  Bartłomiej Duda
License: GPL-3.0 License
"""
import os

import pytest

from reversebox.io_files.file_handler import FileHandler


@pytest.mark.unittest
def test_check_file_size():
    file_path = os.path.join(
        os.path.dirname(__file__), "data\\fake_file7_check_size_11_bytes.bin"
    )

    file_reader = FileHandler(file_path, "rb")
    file_reader.open()

    file_reader.read_str(4, "utf8")

    current_offset1 = file_reader.get_position()
    file_size = file_reader.get_file_size()
    current_offset2 = file_reader.get_position()

    assert file_size == 11
    assert current_offset1 == 4
    assert current_offset2 == 4
