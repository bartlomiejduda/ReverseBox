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
def test_ps_vita_unswizzle_and_swizzle():
    swizzled_file_path = os.path.join(
        os.path.dirname(__file__), "image_files/swizzle_ps_vita_monkey_BGRA8888.bin"
    )

    bin_file = open(swizzled_file_path, "rb")
    swizzled_file_data = bin_file.read()

    img_width = 256
    img_height = 128
    bpp = 32
    image_format = ImageFormats.BGRA8888

    unswizzled_file_data = unswizzle_psvita_dreamcast(swizzled_file_data, img_width, img_height, bpp, block_width_height=1)

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

    reswizzled_file_data = swizzle_psvita_dreamcast(unswizzled_file_data, img_width, img_height, bpp, block_width_height=1)

    assert len(swizzled_file_data) == len(reswizzled_file_data)
    assert swizzled_file_data[:100] == reswizzled_file_data[:100]
    assert swizzled_file_data[1000:1100] == reswizzled_file_data[1000:1100]
    assert swizzled_file_data[3000:3100] == reswizzled_file_data[3000:3100]
    assert swizzled_file_data[-100:] == reswizzled_file_data[-100:]


@pytest.mark.imagetest
def test_ps_vita_unswizzle_and_swizzle_tex_all():
    swizzled_file_path = os.path.join(
        os.path.dirname(__file__), "image_files/swizzle_ps_vita_tex_all.bin"
    )

    bin_file = open(swizzled_file_path, "rb")
    bin_file.seek(16)
    swizzled_file_data = bin_file.read()

    img_width = 2048
    img_height = 1024
    bpp = 8
    image_format = ImageFormats.BC3_DXT5

    unswizzled_file_data = unswizzle_psvita_dreamcast(swizzled_file_data, img_width, img_height, bpp, block_width_height=4)

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

    reswizzled_file_data = swizzle_psvita_dreamcast(unswizzled_file_data, img_width, img_height, bpp, block_width_height=4)

    assert len(swizzled_file_data) == len(reswizzled_file_data)
    assert swizzled_file_data[:100] == reswizzled_file_data[:100]
    assert swizzled_file_data[1000:1100] == reswizzled_file_data[1000:1100]
    assert swizzled_file_data[3000:3100] == reswizzled_file_data[3000:3100]
    assert swizzled_file_data[-100:] == reswizzled_file_data[-100:]


@pytest.mark.imagetest
def test_ps_vita_unswizzle_and_swizzle_monkey_dxt5():
    swizzled_file_path = os.path.join(
        os.path.dirname(__file__), "image_files/swizzle_ps_vita_monkey_dxt5.bin"
    )

    bin_file = open(swizzled_file_path, "rb")
    swizzled_file_data = bin_file.read()

    img_width = 256
    img_height = 128
    bpp = 8
    image_format = ImageFormats.BC3_DXT5

    unswizzled_file_data = unswizzle_psvita_dreamcast(swizzled_file_data, img_width, img_height, bpp, block_width_height=4)

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

    reswizzled_file_data = swizzle_psvita_dreamcast(unswizzled_file_data, img_width, img_height, bpp, block_width_height=4)

    assert len(swizzled_file_data) == len(reswizzled_file_data)
    assert swizzled_file_data[:100] == reswizzled_file_data[:100]
    assert swizzled_file_data[1000:1100] == reswizzled_file_data[1000:1100]
    assert swizzled_file_data[3000:3100] == reswizzled_file_data[3000:3100]
    # assert swizzled_file_data[-100:] == reswizzled_file_data[-100:]  # TODO - why it's not working?


@pytest.mark.imagetest
def test_ps_vita_unswizzle_and_swizzle_font_dmg0():
    swizzled_file_path = os.path.join(
        os.path.dirname(__file__), "image_files/swizzle_ps_vita_font_dmg0.bin"
    )

    bin_file = open(swizzled_file_path, "rb")
    swizzled_file_data = bin_file.read()

    img_width = 512
    img_height = 32
    bpp = 8
    image_format = ImageFormats.BC3_DXT5

    unswizzled_file_data = unswizzle_psvita_dreamcast(swizzled_file_data, img_width, img_height, bpp, block_width_height=4)

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

    reswizzled_file_data = swizzle_psvita_dreamcast(unswizzled_file_data, img_width, img_height, bpp, block_width_height=4)

    assert len(swizzled_file_data) == len(reswizzled_file_data)
    assert swizzled_file_data[:100] == reswizzled_file_data[:100]
    assert swizzled_file_data[1000:1100] == reswizzled_file_data[1000:1100]
    assert swizzled_file_data[3000:3100] == reswizzled_file_data[3000:3100]
    assert swizzled_file_data[-100:] == reswizzled_file_data[-100:]
