"""
Copyright © 2024  Bartłomiej Duda
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
def test_decode_and_encode_all_generic_images():

    image_decoder = ImageDecoder()
    image_encoder = ImageEncoder()
    wrapper = PillowWrapper()

    image_test_entries = [
        ImageDecodeEncodeTestEntry(img_file_path="monkey_RGBA8888.bin", debug_flag=False, img_width=256, img_height=128, img_format=ImageFormats.RGBA8888),
        ImageDecodeEncodeTestEntry(img_file_path="monkey_RGB565.bin", debug_flag=False, img_width=256, img_height=128, img_format=ImageFormats.RGB565),
        ImageDecodeEncodeTestEntry(img_file_path="monkey_BGRA8888.bin", debug_flag=False, img_width=256, img_height=128, img_format=ImageFormats.BGRA8888),
        ImageDecodeEncodeTestEntry(img_file_path="monkey_BGR565.bin", debug_flag=False, img_width=256, img_height=128, img_format=ImageFormats.BGR565),
        ImageDecodeEncodeTestEntry(img_file_path="monkey_RGB888.bin", debug_flag=False, img_width=256, img_height=128, img_format=ImageFormats.RGB888),
        ImageDecodeEncodeTestEntry(img_file_path="monkey_BGR888.bin", debug_flag=False, img_width=256, img_height=128, img_format=ImageFormats.BGR888),
        ImageDecodeEncodeTestEntry(img_file_path="monkey_RGBA4444.bin", debug_flag=False, img_width=256, img_height=128, img_format=ImageFormats.RGBA4444),
        ImageDecodeEncodeTestEntry(img_file_path="monkey_ARGB4444.bin", debug_flag=False, img_width=256, img_height=128, img_format=ImageFormats.ARGB4444),
    ]

    for test_entry in image_test_entries:

        bin_file = open(_get_test_image_path(test_entry.img_file_path), "rb")
        encoded_image_data = bin_file.read()
        bin_file.close()
        decoded_image_data: bytes = image_decoder.decode_image(encoded_image_data, test_entry.img_width, test_entry.img_height, test_entry.img_format)
        re_encoded_image_data: bytes = image_encoder.encode_image(decoded_image_data, test_entry.img_width, test_entry.img_height, test_entry.img_format)
        re_decoded_image_data: bytes = image_decoder.decode_image(re_encoded_image_data, test_entry.img_width, test_entry.img_height, test_entry.img_format)

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

        assert decoded_image_data[:100] == re_decoded_image_data[:100]
        assert decoded_image_data[1000:1100] == re_decoded_image_data[1000:1100]
        assert decoded_image_data[3000:3100] == re_decoded_image_data[3000:3100]
        assert decoded_image_data[-100:] == re_decoded_image_data[-100:]

        assert encoded_image_data[:100] == re_encoded_image_data[:100]
        assert encoded_image_data[1000:1100] == re_encoded_image_data[1000:1100]
        assert encoded_image_data[3000:3100] == re_encoded_image_data[3000:3100]
        assert encoded_image_data[-100:] == re_encoded_image_data[-100:]
