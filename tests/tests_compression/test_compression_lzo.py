"""
Copyright © 2022  Bartłomiej Duda
License: GPL-3.0 License
"""

import os

import pytest

from reversebox.compression.compression_lzo import LZOHandler


@pytest.mark.unittest
def test_open_and_compress_file_with_lzo():
    uncompressed_file_path = os.path.join(
        os.path.dirname(__file__), "compression_data\\fake_file02_lzo_uncompressed.bin"
    )
    compressed_file_path = os.path.join(
        os.path.dirname(__file__), "compression_data\\fake_file02_lzo_compressed.bin"
    )

    uncompressed_input_file_data = open(uncompressed_file_path, "rb").read()
    compressed_input_file_data = open(compressed_file_path, "rb").read()

    lzo_handler = LZOHandler()
    compressed_data = lzo_handler.compress_data(uncompressed_input_file_data)

    assert compressed_data == compressed_input_file_data


@pytest.mark.unittest
def test_open_and_decompress_file_with_lzo():
    uncompressed_file_path = os.path.join(
        os.path.dirname(__file__), "compression_data\\fake_file02_lzo_uncompressed.bin"
    )
    compressed_file_path = os.path.join(
        os.path.dirname(__file__), "compression_data\\fake_file02_lzo_compressed.bin"
    )

    uncompressed_input_file_data = open(uncompressed_file_path, "rb").read()
    compressed_input_file_data = open(compressed_file_path, "rb").read()

    lzo_handler = LZOHandler()
    uncompressed_data = lzo_handler.decompress_data(compressed_input_file_data)
    assert uncompressed_data == uncompressed_input_file_data
