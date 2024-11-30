"""
Copyright © 2024  Bartłomiej Duda
License: GPL-3.0 License
"""

import os

import pytest

from reversebox.image.image_decoder import ImageDecoder
from reversebox.image.image_formats import ImageFormats
from reversebox.image.pillow_wrapper import PillowWrapper
from reversebox.image.swizzling.swizzle_ps2 import (
    swizzle_ps2,
    swizzle_ps2_ea_4bit,
    unswizzle_ps2,
    unswizzle_ps2_ea_4bit,
    unswizzle_ps2_palette,
)

# fmt: off


@pytest.mark.imagetest
def test_ps2_unswizzle_and_swizzle_8bit():
    swizzled_file_path = os.path.join(os.path.dirname(__file__), "image_files/ps2_swizzle_8bit_monkey_data.bin")
    palette_file_path = os.path.join(os.path.dirname(__file__), "image_files/ps2_swizzle_8bit_monkey_palette.bin")

    swizzled_file_data = open(swizzled_file_path, "rb").read()
    palette_data = open(palette_file_path, "rb").read()

    img_width = 256
    img_height = 128
    bpp = 8
    image_format = ImageFormats.PAL8_RGBA8888

    unswizzled_file_data = unswizzle_ps2(
        swizzled_file_data, img_width, img_height, bpp
    )

    # debug start ###############################################################################################
    is_debug = False
    if is_debug:
        image_decoder = ImageDecoder()
        wrapper = PillowWrapper()
        unswizzled_palette_data = unswizzle_ps2_palette(palette_data)
        decoded_image_data: bytes = image_decoder.decode_indexed_image(
            unswizzled_file_data, unswizzled_palette_data, img_width, img_height, image_format
        )
        pil_image = wrapper.get_pillow_image_from_rgba8888_data(decoded_image_data, img_width, img_height)
        pil_image.show()
    # debug end #################################################################################################

    reswizzled_file_data = swizzle_ps2(
        unswizzled_file_data, img_width, img_height, bpp
    )

    assert swizzled_file_data[:10] == reswizzled_file_data[:10]
    assert swizzled_file_data[1000:1100] == reswizzled_file_data[1000:1100]
    assert swizzled_file_data[3000:3100] == reswizzled_file_data[3000:3100]
    assert swizzled_file_data[-100:] == reswizzled_file_data[-100:]


# this sample uses special "type 3" 4-bit PS2 swizzle function
@pytest.mark.imagetest
def test_ps2_unswizzle_and_swizzle_4bit():
    swizzled_file_path = os.path.join(os.path.dirname(__file__), "image_files/ps2_swizzle_4bit_monkey_data.bin")
    palette_file_path = os.path.join(os.path.dirname(__file__), "image_files/ps2_swizzle_4bit_monkey_palette.bin")

    swizzled_file_data = open(swizzled_file_path, "rb").read()
    palette_data = open(palette_file_path, "rb").read()

    img_width = 256
    img_height = 128
    bpp = 4
    image_format = ImageFormats.PAL4_RGBA8888

    unswizzled_file_data = unswizzle_ps2_ea_4bit(
        swizzled_file_data, img_width, img_height, bpp
    )

    # debug start ###############################################################################################
    is_debug = False
    if is_debug:
        image_decoder = ImageDecoder()
        wrapper = PillowWrapper()
        unswizzled_palette_data = unswizzle_ps2_palette(palette_data)
        decoded_image_data: bytes = image_decoder.decode_indexed_image(
            unswizzled_file_data, unswizzled_palette_data, img_width, img_height, image_format
        )
        pil_image = wrapper.get_pillow_image_from_rgba8888_data(decoded_image_data, img_width, img_height)
        pil_image.show()
    # debug end #################################################################################################

    reswizzled_file_data = swizzle_ps2_ea_4bit(
        unswizzled_file_data, img_width, img_height, bpp
    )

    assert swizzled_file_data[:10] == reswizzled_file_data[:10]
    assert swizzled_file_data[1000:1100] == reswizzled_file_data[1000:1100]
    assert swizzled_file_data[3000:3100] == reswizzled_file_data[3000:3100]
    assert swizzled_file_data[-100:] == reswizzled_file_data[-100:]


# fmt: on
