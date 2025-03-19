"""
Copyright © 2024-2025  Bartłomiej Duda
License: GPL-3.0 License
"""

import os

import pytest

from reversebox.image.image_decoder import ImageDecoder
from reversebox.image.image_formats import ImageFormats
from reversebox.image.pillow_wrapper import PillowWrapper
from reversebox.image.swizzling.swizzle_morton_ps4 import swizzle_ps4, unswizzle_ps4

# fmt: off


@pytest.mark.imagetest
def test_ps4_unswizzle_and_swizzle():
    swizzled_file_path = os.path.join(
        os.path.dirname(__file__), "image_files/swizzle_ps4_DXT5.bin"
    )

    bin_file = open(swizzled_file_path, "rb")
    bin_file.seek(32)
    swizzled_file_data = bin_file.read()

    img_width = 2048
    img_height = 2048
    block_width = 4
    block_height = 4
    block_data_size = 16
    image_format = ImageFormats.BC3_DXT5

    unswizzled_file_data = unswizzle_ps4(
        swizzled_file_data, img_width, img_height, block_width, block_height, block_data_size
    )

    # debug start ###############################################################################################
    is_debug = False
    if is_debug:
        image_decoder = ImageDecoder()
        wrapper = PillowWrapper()
        decoded_image_data: bytes = image_decoder.decode_compressed_image(
            unswizzled_file_data, img_width, img_height, image_format
        )
        pil_image = wrapper.get_pillow_image_from_rgba8888_data(decoded_image_data, img_width, img_height)
        pil_image.show()
    # debug end #################################################################################################

    reswizzled_file_data = swizzle_ps4(
        unswizzled_file_data, img_width, img_height, block_width, block_height, block_data_size
    )

    assert len(swizzled_file_data) == len(reswizzled_file_data)
    assert swizzled_file_data[:100] == reswizzled_file_data[:100]
    assert swizzled_file_data[1000:1100] == reswizzled_file_data[1000:1100]
    assert swizzled_file_data[3000:3100] == reswizzled_file_data[3000:3100]
    assert swizzled_file_data[-100:] == reswizzled_file_data[-100:]
