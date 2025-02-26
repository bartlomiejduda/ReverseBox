"""
Copyright © 2025 Bartłomiej Duda
License: GPL-3.0 License
"""

import os

import pytest

from reversebox.image.image_decoder import ImageDecoder
from reversebox.image.image_formats import ImageFormats
from reversebox.image.pillow_wrapper import PillowWrapper
from tests.common import ImageDecodeEncodeTestEntry

# fmt: off


def _get_test_image_path(file_name: str) -> str:
    return os.path.join(os.path.dirname(__file__), f"image_files/{file_name}")


@pytest.mark.imagetest
def test_decode_and_encode_all_indexed_images():

    image_decoder = ImageDecoder()
    wrapper = PillowWrapper()

    image_test_entries = [
        ImageDecodeEncodeTestEntry(img_file_path="pal_i8a8_bgra8888.bin", debug_flag=False, img_width=256, img_height=120,
                                   bpp=16, img_format=ImageFormats.PAL_I8A8, pal_format=ImageFormats.BGRA8888,
                                   palette_offset=48, palette_size=1024, image_data_offset=1072, image_data_size=61440),
    ]

    for test_entry in image_test_entries:

        bin_file = open(_get_test_image_path(test_entry.img_file_path), "rb")

        bin_file.seek(test_entry.palette_offset)
        palette_data: bytes = bin_file.read(test_entry.palette_size)

        bin_file.seek(test_entry.image_data_offset)
        image_file_data: bytes = bin_file.read(test_entry.image_data_size)

        decoded_image_data: bytes = image_decoder.decode_indexed_image(image_file_data, palette_data, test_entry.img_width, test_entry.img_height, test_entry.img_format, test_entry.pal_format)

        # debug start ###############################################################################################
        if test_entry.debug_flag:
            pil_image = wrapper.get_pillow_image_from_rgba8888_data(decoded_image_data, test_entry.img_width, test_entry.img_height)
            pil_image.show()
        # debug end #################################################################################################

        # TODO - add encoding and more asserts
        assert len(image_file_data) > 0
        assert len(decoded_image_data) > 0
