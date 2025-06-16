"""
Copyright © 2025  Bartłomiej Duda
License: GPL-3.0 License
"""

import os

import pytest

from reversebox.image.image_decoder import ImageDecoder
from reversebox.image.image_encoder import ImageEncoder
from reversebox.image.image_formats import ImageFormats
from reversebox.image.pillow_wrapper import PillowWrapper
from tests.common import ImageDecodeEncodeTestEntry

# fmt: off


def _get_test_image_path(file_name: str) -> str:
    return os.path.join(os.path.dirname(__file__), f"image_files/{file_name}")


@pytest.mark.imagetest
def test_decode_and_encode_all_pvrtexlib_images():

    image_decoder = ImageDecoder()
    image_encoder = ImageEncoder()
    wrapper = PillowWrapper()

    image_test_entries = [
        ImageDecodeEncodeTestEntry(img_file_path="monkey_ASTC_4x4.bin", debug_flag=False, img_width=256, img_height=128, bpp=8, img_format=ImageFormats.ASTC_4x4),
        ImageDecodeEncodeTestEntry(img_file_path="monkey_ASTC_5x4.bin", debug_flag=False, img_width=256, img_height=128, bpp=8, img_format=ImageFormats.ASTC_5x4),
        ImageDecodeEncodeTestEntry(img_file_path="monkey_ASTC_5x5.bin", debug_flag=False, img_width=256, img_height=128, bpp=8, img_format=ImageFormats.ASTC_5x5),
        ImageDecodeEncodeTestEntry(img_file_path="monkey_ASTC_6x5.bin", debug_flag=False, img_width=256, img_height=128, bpp=8, img_format=ImageFormats.ASTC_6x5),
        ImageDecodeEncodeTestEntry(img_file_path="monkey_ASTC_6x6.bin", debug_flag=False, img_width=256, img_height=128, bpp=8, img_format=ImageFormats.ASTC_6x6),
        ImageDecodeEncodeTestEntry(img_file_path="monkey_ASTC_8x5.bin", debug_flag=False, img_width=256, img_height=128, bpp=8, img_format=ImageFormats.ASTC_8x5),
        ImageDecodeEncodeTestEntry(img_file_path="monkey_ASTC_8x6.bin", debug_flag=False, img_width=256, img_height=128, bpp=8, img_format=ImageFormats.ASTC_8x6),
        ImageDecodeEncodeTestEntry(img_file_path="monkey_ASTC_8x8.bin", debug_flag=False, img_width=256, img_height=128, bpp=8, img_format=ImageFormats.ASTC_8x8),
        ImageDecodeEncodeTestEntry(img_file_path="monkey_ASTC_10x5.bin", debug_flag=False, img_width=256, img_height=128, bpp=8, img_format=ImageFormats.ASTC_10x5),
        ImageDecodeEncodeTestEntry(img_file_path="monkey_ASTC_10x6.bin", debug_flag=False, img_width=256, img_height=128, bpp=8, img_format=ImageFormats.ASTC_10x6),
        ImageDecodeEncodeTestEntry(img_file_path="monkey_ASTC_10x8.bin", debug_flag=False, img_width=256, img_height=128, bpp=8, img_format=ImageFormats.ASTC_10x8),
        ImageDecodeEncodeTestEntry(img_file_path="monkey_ASTC_10x10.bin", debug_flag=False, img_width=256, img_height=128, bpp=8, img_format=ImageFormats.ASTC_10x10),
        ImageDecodeEncodeTestEntry(img_file_path="monkey_ASTC_12x10.bin", debug_flag=False, img_width=256, img_height=128, bpp=8, img_format=ImageFormats.ASTC_12x10),
        ImageDecodeEncodeTestEntry(img_file_path="monkey_ASTC_12x12.bin", debug_flag=False, img_width=256, img_height=128, bpp=8, img_format=ImageFormats.ASTC_12x12),
        ImageDecodeEncodeTestEntry(img_file_path="monkey_ETC1.bin", debug_flag=False, img_width=256, img_height=128, bpp=8, img_format=ImageFormats.ETC1),
        ImageDecodeEncodeTestEntry(img_file_path="monkey_RGBM.bin", debug_flag=False, img_width=256, img_height=128, bpp=8, img_format=ImageFormats.RGBM),
    ]

    for test_entry in image_test_entries:

        bin_file = open(_get_test_image_path(test_entry.img_file_path), "rb")
        encoded_image_data = bin_file.read()

        decoded_image_data: bytes = image_decoder.decode_pvrtexlib_image(encoded_image_data, test_entry.img_width, test_entry.img_height, test_entry.img_format)
        re_encoded_image_data: bytes = image_encoder.encode_pvrtexlib_image(decoded_image_data, test_entry.img_width, test_entry.img_height, test_entry.img_format)
        re_decoded_image_data: bytes = image_decoder.decode_pvrtexlib_image(re_encoded_image_data, test_entry.img_width, test_entry.img_height, test_entry.img_format)

        # debug start ###############################################################################################
        if test_entry.debug_flag:
            pil_image = wrapper.get_pillow_image_from_rgba8888_data(re_decoded_image_data, test_entry.img_width, test_entry.img_height)
            pil_image.show()
        # debug end #################################################################################################

        assert len(encoded_image_data) > 0
        assert len(decoded_image_data) > 0
        assert len(re_encoded_image_data) > 0
        assert len(re_decoded_image_data) > 0
        assert len(decoded_image_data) == len(re_decoded_image_data)
        assert len(encoded_image_data) == len(re_encoded_image_data)
