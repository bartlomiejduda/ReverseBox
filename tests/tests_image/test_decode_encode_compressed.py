"""
Copyright © 2024  Bartłomiej Duda
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
def test_decode_and_encode_all_compressed_images():

    image_decoder = ImageDecoder()
    wrapper = PillowWrapper()

    image_test_entries = [
        ImageDecodeEncodeTestEntry(img_file_path="monkey_dxt1.bin", debug_flag=False, img_width=256, img_height=128, bpp=8, img_format=ImageFormats.BC1_DXT1),
        ImageDecodeEncodeTestEntry(img_file_path="monkey_dxt3.bin", debug_flag=False, img_width=256, img_height=128, bpp=8, img_format=ImageFormats.BC2_DXT3),
        ImageDecodeEncodeTestEntry(img_file_path="monkey_dxt5.bin", debug_flag=False, img_width=256, img_height=128, bpp=8, img_format=ImageFormats.BC3_DXT5),
    ]

    for test_entry in image_test_entries:

        bin_file = open(_get_test_image_path(test_entry.img_file_path), "rb")
        image_file_data = bin_file.read()

        decoded_image_data: bytes = image_decoder.decode_compressed_image(image_file_data, test_entry.img_width, test_entry.img_height, test_entry.img_format)

        # debug start ###############################################################################################
        if test_entry.debug_flag:
            pil_image = wrapper.get_pillow_image_from_rgba8888_data(decoded_image_data, test_entry.img_width, test_entry.img_height)
            pil_image.show()
        # debug end #################################################################################################

        # TODO - add encoding and more asserts
        assert len(image_file_data) > 0
        assert len(decoded_image_data) > 0
