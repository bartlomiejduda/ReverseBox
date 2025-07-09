"""
Copyright © 2024  Bartłomiej Duda
License: GPL-3.0 License
"""

import os

import pytest

from reversebox.image.decoders.gst_decoder_encoder import GSTImageDecoderEncoder
from reversebox.image.image_decoder import ImageDecoder
from reversebox.image.image_formats import ImageFormats
from reversebox.image.pillow_wrapper import PillowWrapper
from reversebox.image.swizzling.swizzle_gst import (
    swizzle_gst_base,
    swizzle_gst_detail1,
    swizzle_gst_detail2,
    unswizzle_gst_base,
    unswizzle_gst_detail1,
    unswizzle_gst_detail2,
)
from tests.common import GSTSwizzleTestEntry

# fmt: off


@pytest.mark.imagetest
def test_gst_unswizzle_and_swizzle():
    gst_test_entries = [
        GSTSwizzleTestEntry(img_path="swizzle_GST121.bin", pal_path="swizzle_GST121.pal", debug_flag=False,
                            img_width=256, img_height=128, img_format=ImageFormats.GST121,
                            conv_format=ImageFormats.PAL8, conv_pal_format=ImageFormats.BGRA8888),

        GSTSwizzleTestEntry(img_path="swizzle_GST122.bin", pal_path="swizzle_GST122.pal", debug_flag=False,
                            img_width=256, img_height=128, img_format=ImageFormats.GST122,
                            conv_format=ImageFormats.PAL8, conv_pal_format=ImageFormats.BGRA8888)
        ]

    for test_entry in gst_test_entries:

        swizzled_file_path = os.path.join(os.path.dirname(__file__), "image_files", test_entry.img_path)
        pal_file_path = os.path.join(os.path.dirname(__file__), "image_files", test_entry.pal_path)

        bin_file = open(swizzled_file_path, "rb")
        swizzled_file_data = bin_file.read()
        bin_file.close()

        pal_file = open(pal_file_path, "rb")
        palette_data = pal_file.read()
        pal_file.close()

        gst_decoder = GSTImageDecoderEncoder()
        base_data = gst_decoder.get_base_data(swizzled_file_data, test_entry.img_width, test_entry.img_height, test_entry.img_format)
        detail_data = gst_decoder.get_detail_data(swizzled_file_data, test_entry.img_width, test_entry.img_height, test_entry.img_format)
        block_width, block_height, detail_bpp = gst_decoder.get_gst_params(test_entry.img_format)

        unswizzled_base_data: bytes = unswizzle_gst_base(base_data, test_entry.img_width, test_entry.img_height, block_width, block_height)
        reswizzled_base_data: bytes = swizzle_gst_base(unswizzled_base_data, test_entry.img_width, test_entry.img_height, block_width, block_height)

        if detail_bpp == 2:
            unswizzled_detail_data: bytes = unswizzle_gst_detail2(detail_data, test_entry.img_width, test_entry.img_height)
            reswizzled_detail_data: bytes = swizzle_gst_detail2(unswizzled_detail_data, test_entry.img_width, test_entry.img_height)
        else:
            unswizzled_detail_data: bytes = unswizzle_gst_detail1(detail_data, test_entry.img_width, test_entry.img_height)
            reswizzled_detail_data: bytes = swizzle_gst_detail1(unswizzled_detail_data, test_entry.img_width, test_entry.img_height)

        # debug start ###############################################################################################
        if test_entry.debug_flag:
            image_decoder = ImageDecoder()
            wrapper = PillowWrapper()
            decoded_image_data: bytes = image_decoder.decode_gst_image(swizzled_file_data, palette_data, test_entry.img_width, test_entry.img_height,
                                                                       test_entry.img_format, test_entry.conv_format, test_entry.conv_pal_format, True)
            pil_image = wrapper.get_pillow_image_from_rgba8888_data(decoded_image_data, test_entry.img_width, test_entry.img_height)
            pil_image.show()
        # debug end #################################################################################################

        assert len(base_data) == len(reswizzled_base_data)
        assert len(detail_data) == len(reswizzled_detail_data)

        assert base_data[:100] == reswizzled_base_data[:100]
        assert base_data[1000:1100] == reswizzled_base_data[1000:1100]
        assert base_data[3000:3100] == reswizzled_base_data[3000:3100]
        assert base_data[-100:] == reswizzled_base_data[-100:]

        assert detail_data[:100] == reswizzled_detail_data[:100]
        assert detail_data[1000:1100] == reswizzled_detail_data[1000:1100]
        assert detail_data[3000:3100] == reswizzled_detail_data[3000:3100]
        assert detail_data[-100:] == reswizzled_detail_data[-100:]
