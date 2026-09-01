"""
Copyright © 2024-2025  Bartłomiej Duda
License: GPL-3.0 License
"""

import os

import pytest

from reversebox.image.byte_swap import swap_byte_order_etc1
from reversebox.image.image_decoder import ImageDecoder
from reversebox.image.image_formats import ImageFormats
from reversebox.image.pillow_wrapper import PillowWrapper
from reversebox.image.swizzling.swizzle_3ds import (
    swizzle_3ds,
    swizzle_3ds_blocks,
    unswizzle_3ds,
    unswizzle_3ds_blocks,
)

# fmt: off


@pytest.mark.imagetest
def test_3ds_unswizzle_and_swizzle():
    swizzled_file_path = os.path.join(
        os.path.dirname(__file__), "image_files/swizzle_3ds.bin"
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

    assert len(swizzled_file_data) == len(reswizzled_file_data)
    assert swizzled_file_data[:100] == reswizzled_file_data[:100]
    assert swizzled_file_data[1000:1100] == reswizzled_file_data[1000:1100]
    assert swizzled_file_data[3000:3100] == reswizzled_file_data[3000:3100]
    assert swizzled_file_data[-100:] == reswizzled_file_data[-100:]


@pytest.mark.imagetest
def test_3ds_etc1_block_unswizzle_and_swizzle():
    swizzled_file_path = os.path.join(
        os.path.dirname(__file__), "image_files/swizzle_3ds_ETC1.tex"
    )

    bin_file = open(swizzled_file_path, "rb")
    bin_file.seek(0x80)
    swizzled_file_data = bin_file.read(0x8000)
    bin_file.close()

    img_width = 256
    img_height = 256
    bpp = 4
    image_format = ImageFormats.ETC1

    unswizzled_file_data = unswizzle_3ds_blocks(
        swizzled_file_data, img_width, img_height, bpp, block_width=4, block_height=4
    )

    # debug start ###############################################################################################
    is_debug = False
    if is_debug:
        image_decoder = ImageDecoder()
        wrapper = PillowWrapper()
        decoded_image_data: bytes = image_decoder.decode_pvrtexlib_image(
            swap_byte_order_etc1(unswizzled_file_data), img_width, img_height, image_format
        )
        pil_image = wrapper.get_pillow_image_from_rgba8888_data(decoded_image_data, img_width, img_height)
        pil_image.show()
    # debug end #################################################################################################

    reswizzled_file_data = swizzle_3ds_blocks(
        unswizzled_file_data, img_width, img_height, bpp, block_width=4, block_height=4
    )

    assert len(swizzled_file_data) == len(reswizzled_file_data)
    assert swizzled_file_data[:100] == reswizzled_file_data[:100]
    assert swizzled_file_data[1000:1100] == reswizzled_file_data[1000:1100]
    assert swizzled_file_data[3000:3100] == reswizzled_file_data[3000:3100]
    assert swizzled_file_data[-100:] == reswizzled_file_data[-100:]


def test_etc1_byte_order_swap():
    little_endian_blocks = bytes(range(16))
    big_endian_blocks = bytes(range(7, -1, -1)) + bytes(range(15, 7, -1))

    assert swap_byte_order_etc1(little_endian_blocks) == big_endian_blocks
    assert swap_byte_order_etc1(big_endian_blocks) == little_endian_blocks
