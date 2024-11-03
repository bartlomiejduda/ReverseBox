"""
Copyright © 2024  Bartłomiej Duda
License: GPL-3.0 License
"""
import os

import pytest

from reversebox.image.image_decoder import ImageDecoder
from reversebox.image.image_formats import ImageFormats
from reversebox.image.pillow_wrapper import PillowWrapper
from reversebox.image.swizzling.swizzle_morton import unswizzle_morton

# fmt: off


@pytest.mark.imagetest
def test_morton_unswizzle_and_swizzle():
    swizzled_file_path = os.path.join(
        os.path.dirname(__file__), "image_files/ARGB4444_XBOX_SWIZZLED.bin"
    )

    bin_file = open(swizzled_file_path, "rb")
    swizzled_file_data = bin_file.read()
    bin_file.close()

    unswizzled_file_data = unswizzle_morton(
        swizzled_file_data, 256, 64, 16
    )

    # debug start ###############################################################################################
    is_debug = False
    if is_debug:
        image_decoder = ImageDecoder()
        wrapper = PillowWrapper()
        decoded_image_data: bytes = image_decoder.decode_image(
            unswizzled_file_data, 256, 64, ImageFormats.ARGB4444
        )
        pil_image = wrapper.get_pillow_image_from_rgba8888_data(decoded_image_data, 256, 64)
        pil_image.show()
    # debug end #################################################################################################

    # TODO - not working as expected
    # reswizzled_file_data = swizzle_morton(
    #     unswizzled_file_data, 256, 64, 16
    # )

    # assert swizzled_file_data[:10] == reswizzled_file_data[:10]
    # assert swizzled_file_data[1000:1100] == reswizzled_file_data[1000:1100]
    # assert swizzled_file_data[3000:3100] == reswizzled_file_data[3000:3100]
    # assert swizzled_file_data[-10:] == reswizzled_file_data[-10:]


# fmt: on
