"""
Copyright © 2025  Bartłomiej Duda
License: GPL-3.0 License
"""

import os

import pytest

from reversebox.compression.compression_huffman_intelligent import (
    huffman_decompress_data,
)


@pytest.mark.unittest
def test_open_and_decompress_file_with_huffman_intelligent():
    uncompressed_file_path: str = os.path.join(
        os.path.dirname(__file__), "compression_data\\huffman_intelligent_raw.ini"
    )
    compressed_file_path: str = os.path.join(
        os.path.dirname(__file__),
        "compression_data\\huffman_intelligent_compressed.ini",
    )

    uncompressed_input_file_data = open(uncompressed_file_path, "rb").read()
    compressed_input_file_data = open(compressed_file_path, "rb").read()

    uncompressed_data: bytes = huffman_decompress_data(compressed_input_file_data)
    assert len(uncompressed_data) == len(uncompressed_input_file_data)
    assert uncompressed_data == uncompressed_input_file_data
