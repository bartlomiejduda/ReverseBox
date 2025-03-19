"""
Copyright © 2024-2025  Bartłomiej Duda
License: GPL-3.0 License
"""

import os

import pytest

from reversebox.image.image_decoder import ImageDecoder
from reversebox.image.image_formats import ImageFormats
from reversebox.image.pillow_wrapper import PillowWrapper
from reversebox.image.swizzling.swizzle_x360 import swizzle_x360, unswizzle_x360

# fmt: off


@pytest.mark.imagetest
def test_x360_unswizzle_and_swizzle():
    swizzled_file_path = os.path.join(
        os.path.dirname(__file__), "image_files/swizzle_xbox360_sample1.bin"
    )

    bin_file = open(swizzled_file_path, "rb")
    swizzled_file_data = bin_file.read()
    bin_file.close()

    img_width = 1024
    img_height = 1024
    image_format = ImageFormats.BC1_DXT1

    unswizzled_file_data = unswizzle_x360(
        swizzled_file_data, img_width, img_height, block_pixel_size=4, texel_byte_pitch=8
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

    reswizzled_file_data = swizzle_x360(
        unswizzled_file_data, img_width, img_height, block_pixel_size=4, texel_byte_pitch=8
    )

    assert len(swizzled_file_data) == len(reswizzled_file_data)
    assert swizzled_file_data[:100] == reswizzled_file_data[:100]
    assert swizzled_file_data[1000:1100] == reswizzled_file_data[1000:1100]
    assert swizzled_file_data[3000:3100] == reswizzled_file_data[3000:3100]
    assert swizzled_file_data[-100:] == reswizzled_file_data[-100:]


@pytest.mark.imagetest
def test_x360_unswizzle_and_swizzle_mt_framework_tex():
    swizzled_file_path = os.path.join(
        os.path.dirname(__file__), "image_files/swizzle_xbox360_mt_framework.tex"
    )

    bin_file = open(swizzled_file_path, "rb")
    bin_file.seek(44)
    swizzled_file_data = bin_file.read()
    bin_file.close()

    img_width = 2304
    img_height = 1152
    image_format = ImageFormats.BC2_DXT3

    unswizzled_file_data = unswizzle_x360(
        swizzled_file_data,
        img_width,
        img_height,
        block_pixel_size=4,
        texel_byte_pitch=16,
    )

    # debug start ###############################################################################################
    is_debug = False
    if is_debug:
        image_decoder = ImageDecoder()
        wrapper = PillowWrapper()
        decoded_image_data: bytes = image_decoder.decode_compressed_image(
            unswizzled_file_data, img_width, img_height, image_format
        )
        pil_image = wrapper.get_pillow_image_from_rgba8888_data(
            decoded_image_data, img_width, img_height
        )
        pil_image.show()
    # debug end #################################################################################################

    reswizzled_file_data = swizzle_x360(
        unswizzled_file_data,
        img_width,
        img_height,
        block_pixel_size=4,
        texel_byte_pitch=16,
    )

    assert len(swizzled_file_data) == len(reswizzled_file_data)
    assert swizzled_file_data[:100] == reswizzled_file_data[:100]
    assert swizzled_file_data[1000:1100] == reswizzled_file_data[1000:1100]
    assert swizzled_file_data[3000:3100] == reswizzled_file_data[3000:3100]
    assert swizzled_file_data[-100:] == reswizzled_file_data[-100:]


@pytest.mark.imagetest
def test_x360_unswizzle_and_swizzle_fairy_with_big_boobs():
    swizzled_file_path = os.path.join(
        os.path.dirname(__file__), "image_files/swizzle_xbox360_fairy_with_big_boobs.bin"
    )

    bin_file = open(swizzled_file_path, "rb")
    swizzled_file_data = bin_file.read()
    bin_file.close()

    img_width = 640
    img_height = 480
    image_format = ImageFormats.BC1_DXT1

    unswizzled_file_data = unswizzle_x360(
        swizzled_file_data,
        img_width,
        img_height,
        block_pixel_size=4,
        texel_byte_pitch=8,
    )

    # debug start ###############################################################################################
    is_debug = False
    if is_debug:
        image_decoder = ImageDecoder()
        wrapper = PillowWrapper()
        decoded_image_data: bytes = image_decoder.decode_compressed_image(
            unswizzled_file_data, img_width, img_height, image_format
        )
        pil_image = wrapper.get_pillow_image_from_rgba8888_data(
            decoded_image_data, img_width, img_height
        )
        pil_image.show()
    # debug end #################################################################################################

    # TODO - fix this, doesn't swizzle correctly for this "fairy" sample
    # reswizzled_file_data = swizzle_x360(
    #     unswizzled_file_data,
    #     img_width,
    #     img_height,
    #     block_pixel_size=4,
    #     texel_byte_pitch=8,
    # )

    # assert len(swizzled_file_data) == len(reswizzled_file_data)
    # assert swizzled_file_data[:100] == reswizzled_file_data[:100]
    # assert swizzled_file_data[1000:1100] == reswizzled_file_data[1000:1100]
    # assert swizzled_file_data[3000:3100] == reswizzled_file_data[3000:3100]
    # assert swizzled_file_data[-100:] == reswizzled_file_data[-100:]
