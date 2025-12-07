"""
Copyright © 2024-2025  Bartłomiej Duda
License: GPL-3.0 License
"""

import os
from typing import List

import pytest

from reversebox.image.image_decoder import ImageDecoder
from reversebox.image.image_formats import ImageFormats
from reversebox.image.pillow_wrapper import PillowWrapper
from reversebox.image.swizzling.morton_index import calculate_morton_index
from reversebox.image.swizzling.swizzle_morton import swizzle_morton, unswizzle_morton
from tests.common import MortonIndexTestEntry

# fmt: off


@pytest.mark.imagetest
def test_morton_unswizzle_and_swizzle():
    swizzled_file_path = os.path.join(
        os.path.dirname(__file__), "image_files/swizzle_morton_monkey.bin"
    )

    bin_file = open(swizzled_file_path, "rb")
    swizzled_file_data = bin_file.read()
    bin_file.close()

    img_width = 256
    img_height = 128
    bpp = 32
    image_format = ImageFormats.BGRA8888

    unswizzled_file_data = unswizzle_morton(swizzled_file_data, img_width, img_height, bpp, block_width=1, block_height=1)

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

    reswizzled_file_data = swizzle_morton(unswizzled_file_data, img_width, img_height, bpp, block_width=1, block_height=1)

    assert len(swizzled_file_data) == len(reswizzled_file_data)
    assert swizzled_file_data[:100] == reswizzled_file_data[:100]
    assert swizzled_file_data[1000:1100] == reswizzled_file_data[1000:1100]
    assert swizzled_file_data[3000:3100] == reswizzled_file_data[3000:3100]
    assert swizzled_file_data[-100:] == reswizzled_file_data[-100:]


@pytest.mark.imagetest
def test_morton_index_if_values_are_correct():
    test_entries: List[MortonIndexTestEntry] = [
        MortonIndexTestEntry(t=1, width=64, height=64, expected_result=1),
        MortonIndexTestEntry(t=16, width=64, height=64, expected_result=4),
        MortonIndexTestEntry(t=64, width=64, height=64, expected_result=8),
        MortonIndexTestEntry(t=1, width=16, height=16, expected_result=1),
        MortonIndexTestEntry(t=2, width=16, height=16, expected_result=16),
        MortonIndexTestEntry(t=3, width=16, height=16, expected_result=17),
        MortonIndexTestEntry(t=4, width=16, height=16, expected_result=2),
        MortonIndexTestEntry(t=5, width=16, height=16, expected_result=3),
        MortonIndexTestEntry(t=6, width=16, height=16, expected_result=18),
        MortonIndexTestEntry(t=7, width=16, height=16, expected_result=19),
        MortonIndexTestEntry(t=8, width=16, height=16, expected_result=32),
        MortonIndexTestEntry(t=9, width=16, height=16, expected_result=33),
        MortonIndexTestEntry(t=10, width=16, height=16, expected_result=48),
    ]

    for test_entry in test_entries:
        morton_index_result: int = calculate_morton_index(test_entry.t, test_entry.width, test_entry.height)
        assert morton_index_result == test_entry.expected_result
