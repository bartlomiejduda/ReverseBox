"""
Copyright © 2025  Bartłomiej Duda
License: GPL-3.0 License
"""

import os
import struct

import pytest

from reversebox.compression.compression_rle_tzar import decompress_rle_tzar
from reversebox.image.image_decoder import ImageDecoder
from reversebox.image.image_formats import ImageFormats
from reversebox.image.pillow_wrapper import PillowWrapper

# fmt: off


@pytest.mark.imagetest
def test_decompress_and_compress_rle_tzar_arab_church():
    compressed_file_path = os.path.join(
        os.path.dirname(__file__), "image_files/compression_rle_tzar_arab_church.bin"
    )

    compressed_file = open(compressed_file_path, "rb")

    img_width = 146
    img_height = 135
    bpp = 16
    image_format = ImageFormats.BGRT5551

    signature: bytes = compressed_file.read(4)
    if signature != b" elr":
        raise Exception("Not supported Tzar RLE file!")
    compressed_file.seek(26)
    compressed_size: int = struct.unpack("<I", compressed_file.read(4))[0]
    compressed_file.seek(38)
    compressed_file_data: bytes = compressed_file.read()

    decompressed_file_data: bytes = decompress_rle_tzar(compressed_file_data, img_width, img_height, bpp)

    # debug start ###############################################################################################
    is_debug = False
    if is_debug:
        image_decoder = ImageDecoder()
        wrapper = PillowWrapper()
        decoded_image_data: bytes = image_decoder.decode_image(
            decompressed_file_data, img_width, img_height, image_format,
        )
        pil_image = wrapper.get_pillow_image_from_rgba8888_data(decoded_image_data, img_width, img_height)
        pil_image.show()
    # debug end #################################################################################################

    assert len(decompressed_file_data) > 0
    assert len(decompressed_file_data) > len(compressed_file_data)
    assert len(compressed_file_data) == compressed_size


@pytest.mark.imagetest
def test_decompress_and_compress_rle_tzar_caravan():
    compressed_file_path = os.path.join(
        os.path.dirname(__file__), "image_files/compression_rle_tzar_caravan.bin"
    )

    compressed_file = open(compressed_file_path, "rb")

    img_width = 195
    img_height = 900
    bpp = 8
    image_format = ImageFormats.PAL8
    palette_format = ImageFormats.BGRT8888

    signature: bytes = compressed_file.read(4)
    if signature != b" elr":
        raise Exception("Not supported Tzar RLE file!")
    compressed_file.seek(26)
    compressed_size: int = struct.unpack("<I", compressed_file.read(4))[0]
    compressed_file.seek(38)

    palette_data: bytearray = bytearray()
    for i in range(256):
        rgb_pal_entry = compressed_file.read(3)
        compressed_file.read(1)
        palette_data += rgb_pal_entry + b'\xFF'

    compressed_file_data: bytes = compressed_file.read()

    decompressed_file_data: bytes = decompress_rle_tzar(compressed_file_data, img_width, img_height, bpp)

    # debug start ###############################################################################################
    is_debug = False
    if is_debug:
        image_decoder = ImageDecoder()
        wrapper = PillowWrapper()
        decoded_image_data: bytes = image_decoder.decode_indexed_image(
            decompressed_file_data, palette_data, img_width, img_height, image_format, palette_format
        )
        pil_image = wrapper.get_pillow_image_from_rgba8888_data(decoded_image_data, img_width, img_height)
        pil_image.show()
    # debug end #################################################################################################

    assert len(decompressed_file_data) > 0
    assert len(compressed_file_data) == compressed_size
