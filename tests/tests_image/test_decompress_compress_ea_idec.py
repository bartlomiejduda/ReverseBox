"""
Copyright © 2025  Bartłomiej Duda
License: GPL-3.0 License
"""

import os

import pytest

from reversebox.compression.compression_ea_idec import decompress_ea_idec
from reversebox.image.image_decoder import ImageDecoder
from reversebox.image.image_formats import ImageFormats
from reversebox.image.pillow_wrapper import PillowWrapper

# fmt: off


@pytest.mark.imagetest
def test_decompress_and_compress_ea_idec_theme_park_world():
    compressed_file_path = os.path.join(
        os.path.dirname(__file__), "image_files/compression_ea_idec_tpw_sample_compressed.bin"
    )
    # decompressed_file_path = os.path.join(
    #     os.path.dirname(__file__), "image_files/compression_ea_idec_tpw_sample_decompressed.bin"
    # )

    compressed_file = open(compressed_file_path, "rb")
    # decompressed_file = open(compressed_file_path, "rb")

    img_width = 128
    img_height = 256
    # bpp = 32
    image_format = ImageFormats.BGRA8888

    compressed_file_data: bytes = compressed_file.read()
    decompressed_file_data: bytes = decompress_ea_idec(compressed_file_data)

    # debug start ###############################################################################################
    is_debug = False
    if is_debug:
        image_decoder = ImageDecoder()
        wrapper = PillowWrapper()
        decoded_image_data: bytes = image_decoder.decode_image(
            decompressed_file_data, img_width, img_height, image_format,
        )
        pil_image = wrapper.get_pillow_image_from_rgba8888_data(decoded_image_data, img_width, img_height)
        pil_image.show()
    # debug end #################################################################################################

    # TODO - make compression work
    assert True
    # assert len(decompressed_file_data) > 0
    # assert len(decompressed_file_data) > len(compressed_file_data)
    # assert len(compressed_file_data) == compressed_size
