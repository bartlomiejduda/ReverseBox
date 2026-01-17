"""
Copyright © 2025-2026 Bartłomiej Duda
License: GPL-3.0 License
"""

import os

import pytest

from reversebox.image.image_decoder import ImageDecoder
from reversebox.image.image_encoder import ImageEncoder
from reversebox.image.image_formats import ImageFormats
from reversebox.image.pillow_wrapper import PillowWrapper
from tests.common import EncodeIndexedMethod, ImageDecodeEncodeTestEntry

# fmt: off


def _get_test_image_path(file_name: str) -> str:
    return os.path.join(os.path.dirname(__file__), f"image_files/{file_name}")


@pytest.mark.imagetest
def test_decode_and_encode_all_indexed_images():

    image_decoder = ImageDecoder()
    image_encoder = ImageEncoder()
    wrapper = PillowWrapper()

    image_test_entries = [
        # ImageDecodeEncodeTestEntry(img_file_path="pal_i8a8_bgra8888.bin", debug_flag=False, img_width=256, img_height=120,
        #                            bpp=16, img_format=ImageFormats.PAL_I8A8, pal_format=ImageFormats.BGRA8888,
        #                            palette_offset=48, palette_size=1024, image_data_offset=1072, image_data_size=61440),
        # ImageDecodeEncodeTestEntry(img_file_path="german_flag.gsh_1_direntry_1.bin",
        #                            pal_file_path="german_flag.gsh_1_direntry_1_binattach_1.bin",
        #                            debug_flag=False, img_width=256, img_height=128, bpp=8,
        #                            img_format=ImageFormats.PAL8, pal_format=ImageFormats.IA_X2, max_colors_count=256,
        #                            palette_offset=0, palette_size=1024, image_data_offset=0, image_data_size=32784,
        #                            number_of_mipmaps=0, encode_indexed_method=EncodeIndexedMethod.V1.value),
        ImageDecodeEncodeTestEntry(img_file_path="ea_sample_PAL8_RGBA8888_150x300.bin",
                                   pal_file_path="ea_sample_PAL8_RGBA8888_150x300_palette.bin",
                                   debug_flag=False, img_width=150, img_height=300, bpp=8,
                                   img_format=ImageFormats.PAL8, pal_format=ImageFormats.RGBA8888, max_colors_count=256,
                                   palette_offset=0, palette_size=1024, image_data_offset=0, image_data_size=45000,
                                   number_of_mipmaps=0, encode_indexed_method=EncodeIndexedMethod.V2.value),
        ImageDecodeEncodeTestEntry(img_file_path="ea_sample_PAL4_RGBA8888_256x256.bin",
                                   pal_file_path="ea_sample_PAL4_RGBA8888_256x256_palette.bin",
                                   debug_flag=False, img_width=256, img_height=256, bpp=4,
                                   img_format=ImageFormats.PAL4, pal_format=ImageFormats.RGBA8888, max_colors_count=16,
                                   palette_offset=0, palette_size=64, image_data_offset=0, image_data_size=43520,
                                   number_of_mipmaps=3, encode_indexed_method=EncodeIndexedMethod.V2.value),
    ]

    for test_entry in image_test_entries:

        bin_file = open(_get_test_image_path(test_entry.img_file_path), "rb")

        if test_entry.pal_file_path is not None:
            pal_file = open(_get_test_image_path(test_entry.pal_file_path), "rb")
            encoded_palette_data: bytes = pal_file.read(test_entry.palette_size)
            pal_file.close()
        else:
            bin_file.seek(test_entry.palette_offset)
            encoded_palette_data: bytes = bin_file.read(test_entry.palette_size)

        bin_file.seek(test_entry.image_data_offset)
        encoded_image_data: bytes = bin_file.read(test_entry.image_data_size)
        assert len(encoded_image_data) == test_entry.image_data_size  # not expected buffer size after reading data!

        decoded_image_data: bytes = image_decoder.decode_indexed_image(
            encoded_image_data,
            encoded_palette_data,
            test_entry.img_width,
            test_entry.img_height,
            test_entry.img_format,
            test_entry.pal_format,
            palette_endianess="little"
        )

        if test_entry.encode_indexed_method == EncodeIndexedMethod.V2.value:
            re_encoded_image_data, re_encoded_palette_data = (
                image_encoder.encode_indexed_image_v2(
                    decoded_image_data,
                    None,
                    test_entry.img_width,
                    test_entry.img_height,
                    test_entry.img_format,
                    test_entry.pal_format,
                    max_color_count=test_entry.max_colors_count,
                    number_of_mipmaps=0 if not test_entry.number_of_mipmaps else test_entry.number_of_mipmaps
                )
            )

        else:
            re_encoded_image_data, re_encoded_palette_data = (
                image_encoder.encode_indexed_image(
                    decoded_image_data,
                    test_entry.img_width,
                    test_entry.img_height,
                    test_entry.img_format,
                    test_entry.pal_format,
                    max_color_count=test_entry.max_colors_count,
                    number_of_mipmaps=0 if not test_entry.number_of_mipmaps else test_entry.number_of_mipmaps
                )
            )
        re_decoded_image_data: bytes = image_decoder.decode_indexed_image(
            re_encoded_image_data,
            re_encoded_palette_data,
            test_entry.img_width,
            test_entry.img_height,
            test_entry.img_format,
            test_entry.pal_format
        )

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

        assert len(encoded_palette_data) > 0
        assert len(re_encoded_palette_data) > 0
        assert len(encoded_palette_data) == len(re_encoded_palette_data)
