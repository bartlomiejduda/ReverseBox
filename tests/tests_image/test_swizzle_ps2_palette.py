"""
Copyright © 2024  Bartłomiej Duda
License: GPL-3.0 License
"""

import os

import pytest

from reversebox.image.palettes.palette_random import generate_random_palette
from reversebox.image.swizzling.swizzle_ps2 import (
    swizzle_ps2_palette,
    unswizzle_ps2_palette,
)

# fmt: off


@pytest.mark.imagetest
def test_ps2_palette_unswizzle_and_swizzle():
    swizzled_file_path = os.path.join(
        os.path.dirname(__file__), "image_files/swizzle_ps2_palette.bin"
    )

    swizzled_palette_file = open(swizzled_file_path, "rb")
    swizzled_palette_data = swizzled_palette_file.read()
    swizzled_palette_file.close()

    unswizzled_palette_data = unswizzle_ps2_palette(swizzled_palette_data)
    reswizzled_palette_data = swizzle_ps2_palette(unswizzled_palette_data)

    assert swizzled_palette_data == reswizzled_palette_data
    assert swizzled_palette_data != unswizzled_palette_data


@pytest.mark.imagetest
def test_ps2_palette_unswizzle_and_swizzle_for_randomly_generated_palette():
    for i in range(10):
        random_palette_data = generate_random_palette()
        unswizzled_palette_data = unswizzle_ps2_palette(random_palette_data)
        reswizzled_palette_data = swizzle_ps2_palette(unswizzled_palette_data)
        assert random_palette_data == reswizzled_palette_data
        assert random_palette_data != unswizzled_palette_data

# fmt: on
