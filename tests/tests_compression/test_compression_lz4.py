"""
Copyright © 2025  Bartłomiej Duda
License: GPL-3.0 License
"""

import os

import pytest

from reversebox.compression.compression_lz4 import LZ4Handler


@pytest.mark.unittest
def test_open_and_compress_file_with_lz4():
    uncompressed_file_path = os.path.join(
        os.path.dirname(__file__), "compression_data\\monkey_sample4.png"
    )
    compressed_file_path = os.path.join(
        os.path.dirname(__file__), "compression_data\\monkey_sample4.png.lz4"
    )

    uncompressed_input_file_data = open(uncompressed_file_path, "rb").read()
    compressed_input_file_data = open(compressed_file_path, "rb").read()

    lz4_handler = LZ4Handler()
    compressed_data = lz4_handler.compress_data(uncompressed_input_file_data)

    assert len(uncompressed_input_file_data) > 0
    assert len(compressed_input_file_data) > 0
    assert len(compressed_data) > 0


@pytest.mark.unittest
def test_open_and_decompress_file_with_lz4():
    uncompressed_file_path = os.path.join(
        os.path.dirname(__file__), "compression_data\\monkey_sample4.png"
    )
    compressed_file_path = os.path.join(
        os.path.dirname(__file__), "compression_data\\monkey_sample4.png.lz4"
    )

    uncompressed_input_file_data = open(uncompressed_file_path, "rb").read()
    compressed_input_file_data = open(compressed_file_path, "rb").read()

    lz4_handler = LZ4Handler()
    uncompressed_data = lz4_handler.decompress_data(compressed_input_file_data)
    assert uncompressed_data == uncompressed_input_file_data
