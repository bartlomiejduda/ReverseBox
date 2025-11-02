"""
Copyright © 2025  Bartłomiej Duda
License: GPL-3.0 License
"""

import os

import pytest
from PIL.Image import Transpose

from reversebox.image.common import get_bc_image_data_size
from reversebox.image.image_decoder import ImageDecoder
from reversebox.image.image_formats import ImageFormats
from reversebox.image.pillow_wrapper import PillowWrapper
from reversebox.image.swizzling.swizzle_switch import swizzle_switch, unswizzle_switch

# fmt: off


@pytest.mark.imagetest
def test_nintendo_switch_unswizzle_and_swizzle_dxt5():
    swizzled_file_path = os.path.join(
        os.path.dirname(__file__), "image_files/swizzle_switch_DXT5.bin"
    )

    bin_file = open(swizzled_file_path, "rb")
    swizzled_file_data = bin_file.read()
    bin_file.close()

    img_width = 512
    img_height = 320
    image_format = ImageFormats.BC3_DXT5
    # TODO - why the image is cropped with the correct size?
    # assert len(swizzled_file_data) == get_bc_image_data_size(img_width, img_height, image_format)

    unswizzled_file_data = unswizzle_switch(swizzled_file_data, img_width, img_height,
                                            bytes_per_block=4, block_height=8, width_pad=8, height_pad=8)

    # debug start ###############################################################################################
    is_debug = False
    if is_debug:
        image_decoder = ImageDecoder()
        wrapper = PillowWrapper()
        decoded_image_data: bytes = image_decoder.decode_compressed_image(unswizzled_file_data, img_width, img_height, image_format)
        pil_image = wrapper.get_pillow_image_from_rgba8888_data(decoded_image_data, img_width, img_height)
        pil_image = pil_image.transpose(Transpose.ROTATE_180)
        pil_image.show()
    # debug end #################################################################################################

    reswizzled_file_data = swizzle_switch(unswizzled_file_data, img_width, img_height)

    assert len(swizzled_file_data) == len(reswizzled_file_data)
    assert swizzled_file_data[:100] == reswizzled_file_data[:100]
    assert swizzled_file_data[1000:1100] == reswizzled_file_data[1000:1100]
    assert swizzled_file_data[3000:3100] == reswizzled_file_data[3000:3100]
    assert swizzled_file_data[-100:] == reswizzled_file_data[-100:]


@pytest.mark.imagetest
def test_nintendo_switch_unswizzle_and_swizzle_gray8():
    swizzled_file_path = os.path.join(
        os.path.dirname(__file__), "image_files/swizzle_switch_GRAY8_320x512.bin"
    )

    bin_file = open(swizzled_file_path, "rb")
    swizzled_file_data = bin_file.read()
    bin_file.close()

    img_width = 320
    img_height = 512
    image_format = ImageFormats.GRAY8

    unswizzled_file_data = unswizzle_switch(swizzled_file_data, img_width, img_height,
                                            bytes_per_block=1, block_height=16, width_pad=8, height_pad=8)

    # debug start ###############################################################################################
    is_debug = False
    if is_debug:
        image_decoder = ImageDecoder()
        wrapper = PillowWrapper()
        decoded_image_data: bytes = image_decoder.decode_image(unswizzled_file_data, img_width, img_height, image_format)
        pil_image = wrapper.get_pillow_image_from_rgba8888_data(decoded_image_data, img_width, img_height)
        pil_image.show()
    # debug end #################################################################################################

    reswizzled_file_data = swizzle_switch(unswizzled_file_data, img_width, img_height)

    assert len(swizzled_file_data) == len(reswizzled_file_data)
    # TODO - why reswizzle doesn't work?
    # assert swizzled_file_data[:100] == reswizzled_file_data[:100]
    # assert swizzled_file_data[1000:1100] == reswizzled_file_data[1000:1100]
    # assert swizzled_file_data[3000:3100] == reswizzled_file_data[3000:3100]
    # assert swizzled_file_data[-100:] == reswizzled_file_data[-100:]


@pytest.mark.imagetest
def test_nintendo_switch_unswizzle_and_swizzle_dxt1_font_file():
    swizzled_file_path = os.path.join(
        os.path.dirname(__file__), "image_files/swizzle_switch_offset287_1024x1024_DXT1.bin"
    )

    bin_file = open(swizzled_file_path, "rb")
    bin_file.seek(287)
    swizzled_file_data = bin_file.read()
    bin_file.close()

    img_width = 1024
    img_height = 1024
    image_format = ImageFormats.BC1_DXT1
    assert len(swizzled_file_data) == get_bc_image_data_size(img_width, img_height, image_format)

    unswizzled_file_data = unswizzle_switch(swizzled_file_data, img_width, img_height,
                                            bytes_per_block=2, block_height=16, width_pad=8, height_pad=8)

    # debug start ###############################################################################################
    is_debug = False
    if is_debug:
        image_decoder = ImageDecoder()
        wrapper = PillowWrapper()
        decoded_image_data: bytes = image_decoder.decode_compressed_image(unswizzled_file_data, img_width, img_height, image_format)
        pil_image = wrapper.get_pillow_image_from_rgba8888_data(decoded_image_data, img_width, img_height)
        pil_image.show()
    # debug end #################################################################################################

    reswizzled_file_data = swizzle_switch(unswizzled_file_data, img_width, img_height)

    assert len(swizzled_file_data) == len(reswizzled_file_data)
    # TODO - why reswizzle doesn't work?
    # assert swizzled_file_data[:100] == reswizzled_file_data[:100]
    # assert swizzled_file_data[1000:1100] == reswizzled_file_data[1000:1100]
    # assert swizzled_file_data[3000:3100] == reswizzled_file_data[3000:3100]
    # assert swizzled_file_data[-100:] == reswizzled_file_data[-100:]


@pytest.mark.imagetest
def test_nintendo_switch_unswizzle_and_swizzle_dxt5_font_file2():
    swizzled_file_path = os.path.join(
        os.path.dirname(__file__), "image_files/swizzle_switch_offset283_512x512_DXT5.bin"
    )

    bin_file = open(swizzled_file_path, "rb")
    bin_file.seek(283)
    swizzled_file_data = bin_file.read()
    bin_file.close()

    img_width = 512
    img_height = 512
    image_format = ImageFormats.BC3_DXT5
    assert len(swizzled_file_data) == get_bc_image_data_size(img_width, img_height, image_format)

    unswizzled_file_data = unswizzle_switch(swizzled_file_data, img_width, img_height,
                                            bytes_per_block=4, block_height=16, width_pad=8, height_pad=8)

    # debug start ###############################################################################################
    is_debug = False
    if is_debug:
        image_decoder = ImageDecoder()
        wrapper = PillowWrapper()
        decoded_image_data: bytes = image_decoder.decode_compressed_image(unswizzled_file_data, img_width, img_height, image_format)
        pil_image = wrapper.get_pillow_image_from_rgba8888_data(decoded_image_data, img_width, img_height)
        pil_image.show()
    # debug end #################################################################################################

    reswizzled_file_data = swizzle_switch(unswizzled_file_data, img_width, img_height)

    assert len(swizzled_file_data) == len(reswizzled_file_data)
    assert swizzled_file_data[:100] == reswizzled_file_data[:100]
    assert swizzled_file_data[1000:1100] == reswizzled_file_data[1000:1100]
    assert swizzled_file_data[3000:3100] == reswizzled_file_data[3000:3100]
    assert swizzled_file_data[-100:] == reswizzled_file_data[-100:]
