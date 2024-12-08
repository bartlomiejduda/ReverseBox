"""
Copyright © 2024  Bartłomiej Duda
License: GPL-3.0 License
"""

import os

import pytest

from reversebox.image.image_decoder import ImageDecoder
from reversebox.image.image_formats import ImageFormats
from reversebox.image.pillow_wrapper import PillowWrapper
from reversebox.image.swizzling.swizzle_3ds import swizzle_3ds, unswizzle_3ds

# fmt: off


@pytest.mark.imagetest
def test_3ds_unswizzle_and_swizzle():
    swizzled_file_path = os.path.join(
        os.path.dirname(__file__), "image_files/3ds_swizzle.bin"
    )

    bin_file = open(swizzled_file_path, "rb")
    swizzled_file_data = bin_file.read()

    img_width = 64
    img_height = 1024
    bpp = 16
    image_format = ImageFormats.RGBA4444

    unswizzled_file_data = unswizzle_3ds(swizzled_file_data, img_width, img_height, bpp)

    # debug start ###############################################################################################
    is_debug = False
    if is_debug:
        image_decoder = ImageDecoder()
        wrapper = PillowWrapper()
        decoded_image_data: bytes = image_decoder.decode_image(unswizzled_file_data, img_width, img_height, image_format)
        pil_image = wrapper.get_pillow_image_from_rgba8888_data(decoded_image_data, img_width, img_height)
        pil_image.show()
    # debug end #################################################################################################

    reswizzled_file_data = swizzle_3ds(unswizzled_file_data, img_width, img_height, bpp)

    assert swizzled_file_data[:10] == reswizzled_file_data[:10]
    assert swizzled_file_data[1000:1100] == reswizzled_file_data[1000:1100]
    assert swizzled_file_data[3000:3100] == reswizzled_file_data[3000:3100]
    assert swizzled_file_data[-100:] == reswizzled_file_data[-100:]
