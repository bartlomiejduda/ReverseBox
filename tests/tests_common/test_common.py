"""
Copyright © 2023-2024  Bartłomiej Duda
License: GPL-3.0 License
"""

import pytest

from reversebox.common.common import (
    calculate_padding_length,
    get_file_extension,
    get_file_extension_uppercase,
)
from tests.common import FileExtensionTestEntry, PaddingTestEntry

# fmt: off


@pytest.mark.unittest
def test_common_calculate_padding():
    padding_data_list = [
        PaddingTestEntry(test_offset=10060, test_div=2048, expected_padding=180),
    ]
    for padding_entry in padding_data_list:
        test_result = calculate_padding_length(padding_entry.test_offset, padding_entry.test_div)
        assert test_result == padding_entry.expected_padding


@pytest.mark.unittest
def test_common_get_file_extension():
    extension_entries_list = [
        FileExtensionTestEntry(file_name="file1.dds", expected_file_extension=".dds"),
        FileExtensionTestEntry(file_name="file2.png", expected_file_extension=".png"),
        FileExtensionTestEntry(file_name="file3.bmp.jpg.png.gif", expected_file_extension=".gif"),
        FileExtensionTestEntry(file_name="file4", expected_file_extension=""),
    ]
    for extension_entry in extension_entries_list:
        test_result = get_file_extension(extension_entry.file_name)
        assert test_result == extension_entry.expected_file_extension


@pytest.mark.unittest
def test_common_get_file_extension_uppercase():
    extension_entries_list = [
        FileExtensionTestEntry(file_name="file1.dds", expected_file_extension="DDS"),
        FileExtensionTestEntry(file_name="file2.png", expected_file_extension="PNG"),
        FileExtensionTestEntry(file_name="file3.bmp.jpg.png.gif", expected_file_extension="GIF"),
        FileExtensionTestEntry(file_name="file4", expected_file_extension=""),
    ]
    for extension_entry in extension_entries_list:
        test_result = get_file_extension_uppercase(extension_entry.file_name)
        assert test_result == extension_entry.expected_file_extension


# fmt: on
