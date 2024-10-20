"""
Copyright © 2024  Bartłomiej Duda
License: GPL-3.0 License
"""
import os

import pytest

from reversebox.image.swizzling.swizzle_psp import swizzle_psp, unswizzle_psp

# fmt: off


@pytest.mark.unittest
def test_psp_unswizzle_and_swizzle():
    swizzled_file_path = os.path.join(
        os.path.dirname(__file__), "image_files\\RGBA8888_PSP_SWIZZLED.bin"
    )

    swizzled_file_data = open(swizzled_file_path, "rb").read()

    unswizzled_file_data = unswizzle_psp(
        swizzled_file_data, 512, 256, 32
    )

    reswizzled_file_data = swizzle_psp(
        unswizzled_file_data, 512, 256, 32
    )

    assert swizzled_file_data[:10] == reswizzled_file_data[:10]
    assert swizzled_file_data[1000:1100] == reswizzled_file_data[1000:1100]
    assert swizzled_file_data[3000:3100] == reswizzled_file_data[3000:3100]
    assert swizzled_file_data[-100:] == reswizzled_file_data[-100:]


# fmt: on
