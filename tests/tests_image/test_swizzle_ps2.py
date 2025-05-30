"""
Copyright © 2024-2025  Bartłomiej Duda
License: GPL-3.0 License
"""

import os

import pytest

from reversebox.image.image_decoder import ImageDecoder
from reversebox.image.image_formats import ImageFormats
from reversebox.image.pillow_wrapper import PillowWrapper
from reversebox.image.swizzling.swizzle_ps2 import (
    swizzle_ps2,
    unswizzle_ps2,
    unswizzle_ps2_palette,
)

# fmt: off


@pytest.mark.imagetest
def test_ps2_unswizzle_and_swizzle_8bit_monkey():
    swizzled_file_path = os.path.join(os.path.dirname(__file__), "image_files/swizzle_ps2_8bit_monkey_data.bin")
    palette_file_path = os.path.join(os.path.dirname(__file__), "image_files/swizzle_ps2_8bit_monkey_palette.bin")

    swizzled_file_data = open(swizzled_file_path, "rb").read()
    palette_data = open(palette_file_path, "rb").read()

    img_width = 256
    img_height = 128
    bpp = 8
    image_format = ImageFormats.PAL8
    pal_format = ImageFormats.RGBA8888

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
            unswizzled_file_data, unswizzled_palette_data, img_width, img_height, image_format, pal_format
        )
        pil_image = wrapper.get_pillow_image_from_rgba8888_data(decoded_image_data, img_width, img_height)
        pil_image.show()
    # debug end #################################################################################################

    reswizzled_file_data = swizzle_ps2(
        unswizzled_file_data, img_width, img_height, bpp
    )

    assert len(swizzled_file_data) == len(reswizzled_file_data)
    assert swizzled_file_data[:10] == reswizzled_file_data[:10]
    assert swizzled_file_data[1000:1100] == reswizzled_file_data[1000:1100]
    assert swizzled_file_data[3000:3100] == reswizzled_file_data[3000:3100]
    assert swizzled_file_data[-100:] == reswizzled_file_data[-100:]


@pytest.mark.imagetest
def test_ps2_unswizzle_and_swizzle_8bit_sample1():
    swizzled_file_path = os.path.join(os.path.dirname(__file__), "image_files/swizzle_ps2_8bit_sample1_512_x256_data.bin")
    palette_file_path = os.path.join(os.path.dirname(__file__), "image_files/swizzle_ps2_8bit_sample1_512_x256_pal.bin")

    swizzled_file_data = open(swizzled_file_path, "rb").read()
    palette_data = open(palette_file_path, "rb").read()

    img_width = 512
    img_height = 256
    bpp = 8
    image_format = ImageFormats.PAL8
    pal_format = ImageFormats.RGBA8888

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
            unswizzled_file_data, unswizzled_palette_data, img_width, img_height, image_format, pal_format
        )
        pil_image = wrapper.get_pillow_image_from_rgba8888_data(decoded_image_data, img_width, img_height)
        pil_image.show()
    # debug end #################################################################################################

    reswizzled_file_data = swizzle_ps2(
        unswizzled_file_data, img_width, img_height, bpp
    )

    assert len(swizzled_file_data) == len(reswizzled_file_data)
    assert swizzled_file_data[:10] == reswizzled_file_data[:10]
    assert swizzled_file_data[1000:1100] == reswizzled_file_data[1000:1100]
    assert swizzled_file_data[3000:3100] == reswizzled_file_data[3000:3100]
    assert swizzled_file_data[-100:] == reswizzled_file_data[-100:]


@pytest.mark.imagetest
def test_ps2_unswizzle_and_swizzle_4bit_monkey():
    swizzled_file_path = os.path.join(os.path.dirname(__file__), "image_files/swizzle_ps2_4bit_monkey_data.bin")
    palette_file_path = os.path.join(os.path.dirname(__file__), "image_files/swizzle_ps2_4bit_monkey_palette.bin")

    swizzled_file_data = open(swizzled_file_path, "rb").read()
    palette_data = open(palette_file_path, "rb").read()

    img_width = 256
    img_height = 128
    bpp = 4
    image_format = ImageFormats.PAL4
    pal_format = ImageFormats.RGBA8888

    unswizzled_file_data = unswizzle_ps2(
        swizzled_file_data, img_width, img_height, bpp, swizzle_type=1
    )

    # debug start ###############################################################################################
    is_debug = False
    if is_debug:
        image_decoder = ImageDecoder()
        wrapper = PillowWrapper()
        unswizzled_palette_data = unswizzle_ps2_palette(palette_data)
        decoded_image_data: bytes = image_decoder.decode_indexed_image(
            unswizzled_file_data, unswizzled_palette_data, img_width, img_height, image_format, pal_format
        )
        pil_image = wrapper.get_pillow_image_from_rgba8888_data(decoded_image_data, img_width, img_height)
        pil_image.show()
    # debug end #################################################################################################

    reswizzled_file_data = swizzle_ps2(
        unswizzled_file_data, img_width, img_height, bpp
    )

    assert len(swizzled_file_data) == len(reswizzled_file_data)
    assert swizzled_file_data[:100] == reswizzled_file_data[:100]
    assert swizzled_file_data[1000:1100] == reswizzled_file_data[1000:1100]
    assert swizzled_file_data[3000:3100] == reswizzled_file_data[3000:3100]
    assert swizzled_file_data[-100:] == reswizzled_file_data[-100:]


@pytest.mark.imagetest
def test_ps2_unswizzle_and_swizzle_4bit_sample2():
    swizzled_file_path = os.path.join(os.path.dirname(__file__), "image_files/swizzle_ps2_4bit_sample2_512x512_data.bin")
    palette_file_path = os.path.join(os.path.dirname(__file__), "image_files/swizzle_ps2_4bit_sample2_512x512_pal.bin")

    swizzled_file_data = open(swizzled_file_path, "rb").read()
    palette_data = open(palette_file_path, "rb").read()

    img_width = 512
    img_height = 512
    bpp = 4
    image_format = ImageFormats.PAL4
    pal_format = ImageFormats.RGBA8888

    unswizzled_file_data = unswizzle_ps2(
        swizzled_file_data, img_width, img_height, bpp, swizzle_type=1
    )

    # debug start ###############################################################################################
    is_debug = False
    if is_debug:
        image_decoder = ImageDecoder()
        wrapper = PillowWrapper()
        unswizzled_palette_data = unswizzle_ps2_palette(palette_data)
        decoded_image_data: bytes = image_decoder.decode_indexed_image(
            unswizzled_file_data, unswizzled_palette_data, img_width, img_height, image_format, pal_format
        )
        pil_image = wrapper.get_pillow_image_from_rgba8888_data(decoded_image_data, img_width, img_height)
        pil_image.show()
    # debug end #################################################################################################

    reswizzled_file_data = swizzle_ps2(
        unswizzled_file_data, img_width, img_height, bpp
    )

    assert len(swizzled_file_data) == len(reswizzled_file_data)
    assert swizzled_file_data[:100] == reswizzled_file_data[:100]
    assert swizzled_file_data[1000:1100] == reswizzled_file_data[1000:1100]
    assert swizzled_file_data[3000:3100] == reswizzled_file_data[3000:3100]
    assert swizzled_file_data[-100:] == reswizzled_file_data[-100:]


@pytest.mark.imagetest
def test_ps2_unswizzle_and_swizzle_4bit_busted_sample_type2():
    swizzled_file_path = os.path.join(os.path.dirname(__file__), "image_files/swizzle_ps2_busted_4bpp_256x64.bin")

    swizzled_file = open(swizzled_file_path, "rb")
    swizzled_file_data = swizzled_file.read(8192)
    palette_data = swizzled_file.read(64)

    img_width = 256
    img_height = 64
    bpp = 4
    image_format = ImageFormats.PAL4
    pal_format = ImageFormats.RGBA8888

    unswizzled_file_data = unswizzle_ps2(
        swizzled_file_data, img_width, img_height, bpp, swizzle_type=2
    )

    # debug start ###############################################################################################
    is_debug = False
    if is_debug:
        image_decoder = ImageDecoder()
        wrapper = PillowWrapper()
        unswizzled_palette_data = unswizzle_ps2_palette(palette_data)
        decoded_image_data: bytes = image_decoder.decode_indexed_image(
            unswizzled_file_data, unswizzled_palette_data, img_width, img_height, image_format, pal_format
        )
        pil_image = wrapper.get_pillow_image_from_rgba8888_data(decoded_image_data, img_width, img_height)
        pil_image.show()
    # debug end #################################################################################################

    reswizzled_file_data = swizzle_ps2(
        unswizzled_file_data, img_width, img_height, bpp, swizzle_type=2
    )

    assert len(swizzled_file_data) == len(reswizzled_file_data)
    assert swizzled_file_data[:100] == reswizzled_file_data[:100]
    assert swizzled_file_data[1000:1100] == reswizzled_file_data[1000:1100]
    assert swizzled_file_data[3000:3100] == reswizzled_file_data[3000:3100]
    assert swizzled_file_data[-100:] == reswizzled_file_data[-100:]


@pytest.mark.imagetest
def test_ps2_unswizzle_and_swizzle_suba_swizzle_8bit():
    swizzled_file_path = os.path.join(os.path.dirname(__file__), "image_files/swizzle_ps2_suba_8bit_data.bin")
    palette_file_path = os.path.join(os.path.dirname(__file__), "image_files/swizzle_ps2_suba_8bit_pal.bin")

    swizzled_file_data = open(swizzled_file_path, "rb").read()
    palette_data = open(palette_file_path, "rb").read()

    img_width = 256 * 2
    img_height = 128 * 2
    bpp = 8
    image_format = ImageFormats.PAL8
    pal_format = ImageFormats.RGB888

    unswizzled_file_data = unswizzle_ps2(
        swizzled_file_data, img_width, img_height, bpp, swizzle_type=3
    )

    # debug start ###############################################################################################
    is_debug = False
    if is_debug:
        image_decoder = ImageDecoder()
        wrapper = PillowWrapper()
        unswizzled_palette_data = unswizzle_ps2_palette(palette_data)
        decoded_image_data: bytes = image_decoder.decode_indexed_image(
            unswizzled_file_data, unswizzled_palette_data, img_width, img_height, image_format, pal_format
        )
        pil_image = wrapper.get_pillow_image_from_rgba8888_data(decoded_image_data, img_width, img_height)
        pil_image.show()
    # debug end #################################################################################################

    reswizzled_file_data = swizzle_ps2(
        unswizzled_file_data, img_width, img_height, bpp, swizzle_type=3
    )

    assert len(swizzled_file_data) == len(reswizzled_file_data)
    assert swizzled_file_data[:100] == reswizzled_file_data[:100]
    assert swizzled_file_data[1000:1100] == reswizzled_file_data[1000:1100]
    assert swizzled_file_data[3000:3100] == reswizzled_file_data[3000:3100]
    assert swizzled_file_data[-100:] == reswizzled_file_data[-100:]


@pytest.mark.imagetest
def test_ps2_unswizzle_and_swizzle_suba_swizzle_16bit():
    swizzled_file_path = os.path.join(os.path.dirname(__file__), "image_files/swizzle_ps2_suba_16bit_data.bin")
    palette_file_path = os.path.join(os.path.dirname(__file__), "image_files/swizzle_ps2_suba_16bit_pal.bin")

    swizzled_file_data = open(swizzled_file_path, "rb").read()
    palette_data = open(palette_file_path, "rb").read()

    img_width = 256
    img_height = 256 * 2
    bpp = 16
    image_format = ImageFormats.PAL4
    pal_format = ImageFormats.RGB888

    unswizzled_file_data = unswizzle_ps2(
        swizzled_file_data, img_width, img_height, bpp, swizzle_type=3
    )

    # debug start ###############################################################################################
    is_debug = False
    if is_debug:
        image_decoder = ImageDecoder()
        wrapper = PillowWrapper()
        unswizzled_palette_data = unswizzle_ps2_palette(palette_data)
        decoded_image_data: bytes = image_decoder.decode_indexed_image(
            unswizzled_file_data, unswizzled_palette_data, img_width, img_height, image_format, pal_format
        )
        pil_image = wrapper.get_pillow_image_from_rgba8888_data(decoded_image_data, img_width, img_height)
        pil_image.show()
    # debug end #################################################################################################

    reswizzled_file_data = swizzle_ps2(
        unswizzled_file_data, img_width, img_height, bpp, swizzle_type=3
    )

    assert len(swizzled_file_data) == len(reswizzled_file_data)
    assert swizzled_file_data[:100] == reswizzled_file_data[:100]
    assert swizzled_file_data[1000:1100] == reswizzled_file_data[1000:1100]
    assert swizzled_file_data[3000:3100] == reswizzled_file_data[3000:3100]
    assert swizzled_file_data[-100:] == reswizzled_file_data[-100:]
