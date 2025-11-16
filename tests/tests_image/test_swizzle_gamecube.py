"""
Copyright © 2024-2025  Bartłomiej Duda
License: GPL-3.0 License
"""

import os

import pytest

from reversebox.image.image_decoder import ImageDecoder
from reversebox.image.image_formats import ImageFormats
from reversebox.image.pillow_wrapper import PillowWrapper
from reversebox.image.swizzling.swizzle_gamecube import (
    swizzle_gamecube,
    unswizzle_gamecube,
)

# fmt: off


@pytest.mark.imagetest
def test_gamecube_unswizzle_and_swizzle_bluebar():
    swizzled_file_path = os.path.join(
        os.path.dirname(__file__), "image_files/swizzle_gamecube_bluebar.bin"
    )

    bin_file = open(swizzled_file_path, "rb")
    swizzled_file_data = bin_file.read()
    bin_file.close()

    img_width = 256
    img_height = 28
    bpp = 32
    image_format = ImageFormats.ARGB8888

    unswizzled_file_data = unswizzle_gamecube(
        swizzled_file_data, img_width, img_height, bpp
    )

    # debug start ###############################################################################################
    is_debug = False
    if is_debug:
        image_decoder = ImageDecoder()
        wrapper = PillowWrapper()
        decoded_image_data: bytes = image_decoder.decode_image(
            unswizzled_file_data, img_width, img_height, image_format
        )
        pil_image = wrapper.get_pillow_image_from_rgba8888_data(decoded_image_data, img_width, img_height)
        pil_image.show()
    # debug end #################################################################################################

    reswizzled_file_data = swizzle_gamecube(
        unswizzled_file_data, img_width, img_height, bpp
    )

    assert len(swizzled_file_data) == len(reswizzled_file_data)
    assert swizzled_file_data[:100] == reswizzled_file_data[:100]
    assert swizzled_file_data[1000:1100] == reswizzled_file_data[1000:1100]
    assert swizzled_file_data[3000:3100] == reswizzled_file_data[3000:3100]
    assert swizzled_file_data[-100:] == reswizzled_file_data[-100:]


@pytest.mark.imagetest
def test_gamecube_unswizzle_and_swizzle_font1_4bit():
    swizzled_file_path = os.path.join(
        os.path.dirname(__file__), "image_files/swizzle_gamecube_font1_4bit.bin"
    )

    bin_file = open(swizzled_file_path, "rb")
    swizzled_file_data = bin_file.read()
    bin_file.close()

    img_width = 128
    img_height = 1152
    bpp = 4
    image_format = ImageFormats.N64_I4

    unswizzled_file_data = unswizzle_gamecube(
        swizzled_file_data, img_width, img_height, bpp
    )

    # debug start ###############################################################################################
    is_debug = False
    if is_debug:
        image_decoder = ImageDecoder()
        wrapper = PillowWrapper()
        decoded_image_data: bytes = image_decoder.decode_image(
            unswizzled_file_data, img_width, img_height, image_format, image_endianess="big"
        )
        pil_image = wrapper.get_pillow_image_from_rgba8888_data(decoded_image_data, img_width, img_height)
        pil_image.show()
    # debug end #################################################################################################

    reswizzled_file_data = swizzle_gamecube(
        unswizzled_file_data, img_width, img_height, bpp
    )

    assert len(swizzled_file_data) == len(reswizzled_file_data)
    assert swizzled_file_data[:100] == reswizzled_file_data[:100]
    assert swizzled_file_data[1000:1100] == reswizzled_file_data[1000:1100]
    assert swizzled_file_data[3000:3100] == reswizzled_file_data[3000:3100]
    assert swizzled_file_data[-100:] == reswizzled_file_data[-100:]


@pytest.mark.imagetest
def test_gamecube_unswizzle_and_swizzle_monkey_i4_4bit():
    swizzled_file_path = os.path.join(
        os.path.dirname(__file__), "image_files/swizzle_gamecube_monkey_i4.bin"
    )

    bin_file = open(swizzled_file_path, "rb")
    swizzled_file_data = bin_file.read()
    bin_file.close()

    img_width = 256
    img_height = 128
    bpp = 4
    image_format = ImageFormats.N64_I4

    unswizzled_file_data = unswizzle_gamecube(
        swizzled_file_data, img_width, img_height, bpp
    )

    # debug start ###############################################################################################
    is_debug = False
    if is_debug:
        image_decoder = ImageDecoder()
        wrapper = PillowWrapper()
        decoded_image_data: bytes = image_decoder.decode_image(
            unswizzled_file_data, img_width, img_height, image_format, image_endianess="big"
        )
        pil_image = wrapper.get_pillow_image_from_rgba8888_data(decoded_image_data, img_width, img_height)
        pil_image.show()
    # debug end #################################################################################################

    reswizzled_file_data = swizzle_gamecube(
        unswizzled_file_data, img_width, img_height, bpp
    )

    assert len(swizzled_file_data) == len(reswizzled_file_data)
    assert swizzled_file_data[:100] == reswizzled_file_data[:100]
    assert swizzled_file_data[1000:1100] == reswizzled_file_data[1000:1100]
    assert swizzled_file_data[3000:3100] == reswizzled_file_data[3000:3100]
    assert swizzled_file_data[-100:] == reswizzled_file_data[-100:]
