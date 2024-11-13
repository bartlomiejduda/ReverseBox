"""
Copyright © 2024  Bartłomiej Duda
License: GPL-3.0 License
"""
import os

import pytest

from reversebox.compression.compression_refpack import RefpackHandler


@pytest.mark.unittest
def test_open_and_compress_file_with_refpack():
    uncompressed_file_path = os.path.join(
        os.path.dirname(__file__),
        "compression_data\\fake_file03_refpack_uncompressed.bin",
    )
    compressed_file_path = os.path.join(
        os.path.dirname(__file__),
        "compression_data\\fake_file03_refpack_compressed.bin",
    )

    uncompressed_input_file_data = open(uncompressed_file_path, "rb").read()
    compressed_input_file_data = open(compressed_file_path, "rb").read()

    refpack_handler = RefpackHandler()
    compressed_data = refpack_handler.compress_data(uncompressed_input_file_data)

    assert len(compressed_data) <= len(compressed_input_file_data) + 100
    assert len(compressed_data) > 0
    assert (
        compressed_data[:2] == compressed_input_file_data[:2]
    )  # check for 10FB signature


@pytest.mark.unittest
def test_open_and_decompress_file_with_refpack():
    uncompressed_file_path = os.path.join(
        os.path.dirname(__file__),
        "compression_data\\fake_file03_refpack_uncompressed.bin",
    )
    compressed_file_path = os.path.join(
        os.path.dirname(__file__),
        "compression_data\\fake_file03_refpack_compressed.bin",
    )

    uncompressed_input_file_data = open(uncompressed_file_path, "rb").read()
    compressed_input_file_data = open(compressed_file_path, "rb").read()

    refpack_handler = RefpackHandler()
    uncompressed_data = refpack_handler.decompress_data(compressed_input_file_data)
    assert len(uncompressed_data) == len(uncompressed_input_file_data)
    assert type(uncompressed_data) == type(uncompressed_input_file_data)
    assert uncompressed_data[:10] == uncompressed_input_file_data[:10]
    assert uncompressed_data[-10:] == uncompressed_input_file_data[-10:]
