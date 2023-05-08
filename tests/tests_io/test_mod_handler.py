"""
Copyright © 2023  Bartłomiej Duda
License: GPL-3.0 License
"""
import logging
import os
from typing import List

import pytest

# fmt: off
from reversebox.io_files.mod_handler import ModEntry, ModHandler

mod_memory: List[ModEntry] = [
    ModEntry(file_offset=33, file_size=3, file_relative_path=".\\aaa.txt"),
    ModEntry(file_offset=128, file_size=5, file_relative_path="bbb\\bbb.txt"),
    ModEntry(file_offset=277, file_size=10, file_relative_path="ccc.txt"),
]
# fmt: on


@pytest.mark.unittest
def test_mod_handler_extract_all_files():
    binary_file_path = os.path.join(
        os.path.dirname(__file__), "data\\fake_file9_mod_before.bin"
    )
    output_directory = os.path.join(
        os.path.dirname(__file__), "data\\fake_file9_output_before"
    )
    mod_handler = ModHandler(
        mod_memory=mod_memory,
        archive_file_path=binary_file_path,
        log_level=logging.ERROR,
    )
    result = mod_handler.export_all_files(output_directory=output_directory)
    assert result


@pytest.mark.unittest
def test_mod_handler_import_all_files():
    binary_file_path = os.path.join(
        os.path.dirname(__file__), "data\\fake_file9_mod_after.bin"
    )
    output_directory = os.path.join(
        os.path.dirname(__file__), "data\\fake_file9_output_after"
    )
    mod_handler = ModHandler(
        mod_memory=mod_memory,
        archive_file_path=binary_file_path,
        log_level=logging.ERROR,
    )
    result = mod_handler.import_all_files(output_directory=output_directory)
    assert result
    assert os.path.getsize(binary_file_path) == 500
