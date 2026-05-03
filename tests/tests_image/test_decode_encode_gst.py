"""
Copyright © 2026 Bartłomiej Duda
License: GPL-3.0 License
"""

import os

import pytest

from reversebox.image.image_decoder import ImageDecoder

# from reversebox.image.image_encoder import ImageEncoder
from reversebox.image.image_formats import ImageFormats
from reversebox.image.pillow_wrapper import PillowWrapper
from tests.common import GSTTestEntry

# fmt: off


def _get_test_image_path(file_name: str) -> str:
    return os.path.join(os.path.dirname(__file__), f"image_files/{file_name}")


@pytest.mark.imagetest
def test_decode_and_encode_all_gst_images():

    image_decoder = ImageDecoder()
    # image_encoder = ImageEncoder()
    wrapper = PillowWrapper()

    image_test_entries = [
        GSTTestEntry(img_path="monkey_GST422.bin", pal_path="monkey_GST422.pal", debug_flag=False,
                     img_width=256, img_height=128, img_format=ImageFormats.GST422, is_swizzled=False,
                     conv_format=ImageFormats.PAL8, conv_pal_format=ImageFormats.BGRA8888),
    ]

    for test_entry in image_test_entries:

        bin_file = open(_get_test_image_path(test_entry.img_path), "rb")
        encoded_image_data = bin_file.read()

        pal_file = open(_get_test_image_path(test_entry.pal_path), "rb")
        encoded_palette_data = pal_file.read()

        decoded_image_data: bytes = image_decoder.decode_gst_image(image_data=encoded_image_data,
                                                                   palette_data=encoded_palette_data,
                                                                   img_width=test_entry.img_width,
                                                                   img_height=test_entry.img_height,
                                                                   image_format=test_entry.img_format,
                                                                   convert_format=test_entry.conv_format,
                                                                   convert_pal_format=test_entry.conv_pal_format,
                                                                   is_swizzled=test_entry.is_swizzled
                                                                   )

        # debug start ###############################################################################################
        if test_entry.debug_flag:
            pil_image = wrapper.get_pillow_image_from_rgba8888_data(decoded_image_data, test_entry.img_width, test_entry.img_height)
            pil_image.show()
        # debug end #################################################################################################

        # TODO - add asserts for encoding
        assert len(encoded_image_data) > 0
        assert len(decoded_image_data) > 0
        # assert len(re_encoded_image_data) > 0
        # assert len(re_decoded_image_data) > 0
        # assert len(decoded_image_data) == len(re_decoded_image_data)
        # assert len(encoded_image_data) == len(re_encoded_image_data)
