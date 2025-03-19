"""
Copyright © 2024-2025  Bartłomiej Duda
License: GPL-3.0 License
"""

import os

import pytest

from reversebox.image.image_decoder import ImageDecoder
from reversebox.image.image_formats import ImageFormats
from reversebox.image.pillow_wrapper import PillowWrapper
from reversebox.image.swizzling.swizzle_psvita_dreamcast import (
    swizzle_psvita_dreamcast,
    unswizzle_psvita_dreamcast,
)

# fmt: off


@pytest.mark.imagetest
def test_morton_dreamcast_unswizzle_and_swizzle():
    swizzled_file_path = os.path.join(
        os.path.dirname(__file__), "image_files/swizzle_dreamcast_GRAY8.bin"
    )

    win_file = open(swizzled_file_path, "rb")
    win_file.seek(0x10d84)
    swizzled_file_data = win_file.read(262144)

    img_width = 512
    img_height = 512
    bpp = 8
    image_format = ImageFormats.GRAY8

    unswizzled_file_data = unswizzle_psvita_dreamcast(
        swizzled_file_data, img_width, img_height, bpp
    )

    # debug start ###############################################################################################
    is_debug = False
    if is_debug:
        image_decoder = ImageDecoder()
        wrapper = PillowWrapper()
        decoded_image_data: bytes = image_decoder.decode_image(
            unswizzled_file_data, img_width, img_height, image_format,
        )
        pil_image = wrapper.get_pillow_image_from_rgba8888_data(decoded_image_data, img_width, img_height)
        pil_image.show()
    # debug end #################################################################################################

    reswizzled_file_data = swizzle_psvita_dreamcast(
        unswizzled_file_data, img_width, img_height, bpp
    )

    assert len(swizzled_file_data) == len(reswizzled_file_data)
    assert swizzled_file_data[:100] == reswizzled_file_data[:100]
    assert swizzled_file_data[1000:1100] == reswizzled_file_data[1000:1100]
    assert swizzled_file_data[3000:3100] == reswizzled_file_data[3000:3100]
    assert swizzled_file_data[-100:] == reswizzled_file_data[-100:]
