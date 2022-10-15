"""
Copyright © 2022  Bartłomiej Duda
License: GPL-3.0 License
"""
import os

import pytest

from reversebox.compression.compression_zlib import ZLIBHandler


@pytest.mark.unittest
def test_open_and_compress_file_with_zlib():
    uncompressed_file_path = os.path.join(
        os.path.dirname(__file__), "compression_data\\fake_file01_zlib_uncompressed.bin"
    )
    compressed_file_path = os.path.join(
        os.path.dirname(__file__), "compression_data\\fake_file01_zlib_compressed.bin"
    )

    uncompressed_input_file_data = open(uncompressed_file_path, "rb").read()
    compressed_input_file_data = open(compressed_file_path, "rb").read()

    zlib_handler = ZLIBHandler()
    compressed_data = zlib_handler.compress_data(uncompressed_input_file_data)

    assert compressed_data == compressed_input_file_data


@pytest.mark.unittest
def test_open_and_decompress_file_with_zlib():
    uncompressed_file_path = os.path.join(
        os.path.dirname(__file__), "compression_data\\fake_file01_zlib_uncompressed.bin"
    )
    compressed_file_path = os.path.join(
        os.path.dirname(__file__), "compression_data\\fake_file01_zlib_compressed.bin"
    )

    uncompressed_input_file_data = open(uncompressed_file_path, "rb").read()
    compressed_input_file_data = open(compressed_file_path, "rb").read()

    zlib_handler = ZLIBHandler()
    uncompressed_data = zlib_handler.decompress_data(compressed_input_file_data)
    assert uncompressed_data == uncompressed_input_file_data
