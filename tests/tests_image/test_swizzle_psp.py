"""
Copyright © 2024  Bartłomiej Duda
License: GPL-3.0 License
"""

import os

import pytest

from reversebox.image.image_decoder import ImageDecoder
from reversebox.image.image_formats import ImageFormats
from reversebox.image.pillow_wrapper import PillowWrapper
from reversebox.image.swizzling.swizzle_psp import swizzle_psp, unswizzle_psp

# fmt: off


@pytest.mark.imagetest
def test_psp_unswizzle_and_swizzle():
    swizzled_file_path = os.path.join(
        os.path.dirname(__file__), "image_files/swizzle_psp_RGBA8888.bin"
    )

    swizzled_file_data = open(swizzled_file_path, "rb").read()

    img_width = 512
    img_height = 256
    bpp = 32
    image_format = ImageFormats.RGBA8888

    unswizzled_file_data = unswizzle_psp(
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

    reswizzled_file_data = swizzle_psp(
        unswizzled_file_data, img_width, img_height, bpp
    )

    assert swizzled_file_data[:10] == reswizzled_file_data[:10]
    assert swizzled_file_data[1000:1100] == reswizzled_file_data[1000:1100]
    assert swizzled_file_data[3000:3100] == reswizzled_file_data[3000:3100]
    assert swizzled_file_data[-100:] == reswizzled_file_data[-100:]


# TODO - fix swizzling for bubbles texture
# @pytest.mark.imagetest
# def test_psp_unswizzle_and_swizzle_bubbles():
#     swizzled_file_path = os.path.join(os.path.dirname(__file__), "image_files\\swizzle_psp_bubbles_data.bin")
#     palette_file_path = os.path.join(os.path.dirname(__file__), "image_files\\swizzle_psp_bubbles_palette.bin")
#
#     swizzled_file_data = open(swizzled_file_path, "rb").read()
#     palette_data = open(palette_file_path, "rb").read()
#
#     img_width = 276
#     img_height = 276
#     bpp = 8
#     image_format = ImageFormats.PAL8_RGBA8888
#
#     unswizzled_file_data = unswizzle_psp(
#         swizzled_file_data, img_width, img_height, bpp
#     )
#
#     # debug start ###############################################################################################
#     is_debug = True
#     if is_debug:
#         image_decoder = ImageDecoder()
#         wrapper = PillowWrapper()
#         decoded_image_data: bytes = image_decoder.decode_indexed_image(
#             unswizzled_file_data, palette_data, img_width, img_height, image_format
#         )
#         pil_image = wrapper.get_pillow_image_from_rgba8888_data(decoded_image_data, img_width, img_height)
#         pil_image.show()
#     # debug end #################################################################################################
#
#     reswizzled_file_data = swizzle_psp(
#         unswizzled_file_data, img_width, img_height, bpp
#     )
#
#     assert swizzled_file_data[:10] == reswizzled_file_data[:10]
#     assert swizzled_file_data[1000:1100] == reswizzled_file_data[1000:1100]
#     assert swizzled_file_data[3000:3100] == reswizzled_file_data[3000:3100]
#     assert swizzled_file_data[-100:] == reswizzled_file_data[-100:]

# fmt: on
