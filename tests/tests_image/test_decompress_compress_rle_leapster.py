"""
Copyright © 2025  Bartłomiej Duda
License: GPL-3.0 License
"""

import os

import pytest
from PIL.Image import Transpose

from reversebox.compression.compression_rle_leapster import decompress_rle_leapster
from reversebox.image.image_decoder import ImageDecoder
from reversebox.image.image_formats import ImageFormats
from reversebox.image.pillow_wrapper import PillowWrapper

# fmt: off


@pytest.mark.imagetest
def test_decompress_and_compress_leapster():
    compressed_file_path = os.path.join(
        os.path.dirname(__file__), "image_files/compression_rle_leapster.bin"
    )

    compressed_file = open(compressed_file_path, "rb")

    img_width = 73
    img_height = 66
    bpp = 16
    image_format = ImageFormats.BGRA4444_LEAPSTER
    compressed_file_data: bytes = compressed_file.read()

    decompressed_file_data: bytes = decompress_rle_leapster(compressed_file_data, img_width, img_height, bpp)

    # debug start ###############################################################################################
    is_debug = False
    if is_debug:
        image_decoder = ImageDecoder()
        wrapper = PillowWrapper()
        decoded_image_data: bytes = image_decoder.decode_image(
            decompressed_file_data, img_width, img_height, image_format,
        )
        pil_image = wrapper.get_pillow_image_from_rgba8888_data(decoded_image_data, img_width, img_height)
        pil_image = pil_image.transpose(Transpose.ROTATE_270)
        pil_image.show()
    # debug end #################################################################################################

    assert len(decompressed_file_data) > 0
    assert len(decompressed_file_data) > len(compressed_file_data)
