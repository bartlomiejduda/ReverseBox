"""
Copyright © 2024  Bartłomiej Duda
License: GPL-3.0 License
"""
import os

import pytest

from reversebox.image.image_decoder import ImageDecoder
from reversebox.image.image_formats import ImageFormats
from reversebox.image.pillow_wrapper import PillowWrapper
from reversebox.image.swizzling.swizzle_morton_dreamcast import (
    swizzle_morton_dreamcast,
    unswizzle_morton_dreamcast,
)

# fmt: off


@pytest.mark.imagetest
def test_morton_dreamcast_unswizzle_and_swizzle():
    swizzled_file_path = os.path.join(
        os.path.dirname(__file__), "image_files/GRAY8_DREAMCAST_SWIZZLED.bin"
    )

    win_file = open(swizzled_file_path, "rb")
    win_file.seek(0x10d84)
    swizzled_file_data = win_file.read(262144)

    unswizzled_file_data = unswizzle_morton_dreamcast(
        swizzled_file_data, 512, 512, 8
    )

    # debug start ###############################################################################################
    is_debug = False
    if is_debug:
        image_decoder = ImageDecoder()
        wrapper = PillowWrapper()
        decoded_image_data: bytes = image_decoder.decode_image(
            unswizzled_file_data, 512, 512, ImageFormats.GRAY8, "little",
        )
        pil_image = wrapper.get_pillow_image_from_rgba8888_data(decoded_image_data, 512, 512)
        pil_image.show()
    # debug end #################################################################################################

    reswizzled_file_data = swizzle_morton_dreamcast(
        unswizzled_file_data, 512, 512, 8
    )

    assert swizzled_file_data[:10] == reswizzled_file_data[:10]
    assert swizzled_file_data[1000:1100] == reswizzled_file_data[1000:1100]
    assert swizzled_file_data[3000:3100] == reswizzled_file_data[3000:3100]
    assert swizzled_file_data[-100:] == reswizzled_file_data[-100:]


# fmt: on
