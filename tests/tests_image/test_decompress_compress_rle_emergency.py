"""
Copyright © 2025  Bartłomiej Duda
License: GPL-3.0 License
"""

import os

import pytest

from reversebox.compression.compression_rle_emergency import decompress_rle_emergency
from reversebox.image.image_decoder import ImageDecoder
from reversebox.image.image_formats import ImageFormats
from reversebox.image.pillow_wrapper import PillowWrapper

# fmt: off


@pytest.mark.imagetest
def test_decompress_and_compress_rle_emergency():
    compressed_file_path = os.path.join(
        os.path.dirname(__file__), "image_files/compression_rle_emergency.bin"
    )

    compressed_file = open(compressed_file_path, "rb")

    img_width = 800
    img_height = 600
    bpp = 8
    image_format = ImageFormats.PAL8
    palette_format = ImageFormats.RGB888

    compressed_file_data: bytes = compressed_file.read(41054)
    palette_data: bytes = compressed_file.read(768)

    decompressed_file_data: bytes = decompress_rle_emergency(compressed_file_data, img_width, img_height, bpp)

    # debug start ###############################################################################################
    is_debug = False
    if is_debug:
        image_decoder = ImageDecoder()
        wrapper = PillowWrapper()
        decoded_image_data: bytes = image_decoder.decode_indexed_image(
            decompressed_file_data, palette_data, img_width, img_height, image_format, palette_format, scale_value=4
        )
        pil_image = wrapper.get_pillow_image_from_rgba8888_data(decoded_image_data, img_width, img_height)
        pil_image.show()
    # debug end #################################################################################################

    assert len(decompressed_file_data) > 0
    assert len(decompressed_file_data) > len(compressed_file_data)
