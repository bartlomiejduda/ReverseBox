"""
Copyright © 2024  Bartłomiej Duda
License: GPL-3.0 License
"""
import os

import pytest

from reversebox.image.image_decoder import ImageDecoder
from reversebox.image.image_formats import ImageFormats
from reversebox.image.pillow_wrapper import PillowWrapper
from reversebox.image.swizzling.swizzle_ps4 import swizzle_ps4, unswizzle_ps4

# fmt: off


@pytest.mark.imagetest
def test_ps4_unswizzle_and_swizzle():
    swizzled_file_path = os.path.join(
        os.path.dirname(__file__), "image_files/DXT5_PS4_SWIZZLED.bin"
    )

    bin_file = open(swizzled_file_path, "rb")
    bin_file.seek(32)
    swizzled_file_data = bin_file.read()

    unswizzled_file_data = unswizzle_ps4(
        swizzled_file_data, 2048, 2048, 4, 4, 16
    )

    # debug start ###############################################################################################
    is_debug = False
    if is_debug:
        image_decoder = ImageDecoder()
        wrapper = PillowWrapper()
        decoded_image_data: bytes = image_decoder.decode_compressed_image(
            unswizzled_file_data, 2048, 2048, ImageFormats.DXT5
        )
        pil_image = wrapper.get_pillow_image_from_rgba8888_data(decoded_image_data, 2048, 2048)
        pil_image.show()
    # debug end #################################################################################################

    reswizzled_file_data = swizzle_ps4(
        unswizzled_file_data, 2048, 2048, 4, 4, 16
    )

    assert swizzled_file_data[:10] == reswizzled_file_data[:10]
    assert swizzled_file_data[1000:1100] == reswizzled_file_data[1000:1100]
    assert swizzled_file_data[3000:3100] == reswizzled_file_data[3000:3100]
    assert swizzled_file_data[-100:] == reswizzled_file_data[-100:]


# fmt: on