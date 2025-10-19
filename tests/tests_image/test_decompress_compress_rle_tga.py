"""
Copyright © 2024  Bartłomiej Duda
License: GPL-3.0 License
"""

import os

import pytest

from reversebox.compression.compression_rle_tga import (
    compress_rle_tga,
    decompress_rle_tga,
)
from reversebox.image.image_decoder import ImageDecoder
from reversebox.image.image_formats import ImageFormats
from reversebox.image.pillow_wrapper import PillowWrapper

# fmt: off


@pytest.mark.imagetest
def test_decompress_and_compress_rle_tga():
    compressed_file_path = os.path.join(
        os.path.dirname(__file__), "image_files/compression_rle_tga.bin"
    )

    compressed_file_data = open(compressed_file_path, "rb").read()

    img_width = 256
    img_height = 128
    bpp = 32
    image_format = ImageFormats.BGRA8888

    decompressed_file_data = decompress_rle_tga(compressed_file_data, bpp)
    recompressed_file_data = compress_rle_tga(decompressed_file_data, bpp)
    re_decompressed_file_data = decompress_rle_tga(recompressed_file_data, bpp)

    # debug start ###############################################################################################
    is_debug = False
    if is_debug:
        image_decoder = ImageDecoder()
        wrapper = PillowWrapper()
        decoded_image_data: bytes = image_decoder.decode_image(
            re_decompressed_file_data, img_width, img_height, image_format
        )
        pil_image = wrapper.get_pillow_image_from_rgba8888_data(decoded_image_data, img_width, img_height)
        pil_image.show()
    # debug end #################################################################################################

    assert len(decompressed_file_data) == len(re_decompressed_file_data)
    assert decompressed_file_data[:100] == re_decompressed_file_data[:100]
    assert decompressed_file_data[1000:1100] == re_decompressed_file_data[1000:1100]
    assert decompressed_file_data[3000:3100] == re_decompressed_file_data[3000:3100]
    assert decompressed_file_data[-100:] == re_decompressed_file_data[-100:]

    assert len(compressed_file_data) == len(recompressed_file_data)
    assert compressed_file_data[:100] == recompressed_file_data[:100]
    assert compressed_file_data[1000:1100] == recompressed_file_data[1000:1100]
    assert compressed_file_data[3000:3100] == recompressed_file_data[3000:3100]
    assert compressed_file_data[-100:] == recompressed_file_data[-100:]
