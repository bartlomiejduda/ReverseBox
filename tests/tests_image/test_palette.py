"""
Copyright © 2025  Bartłomiej Duda
License: GPL-3.0 License
"""

import pytest

from reversebox.image.palettes.palette_random import generate_random_palette
from reversebox.image.palettes.palette_vga import get_vga_palette

# fmt: off


@pytest.mark.imagetest
def test_get_random_palette():
    palette_1: bytes = generate_random_palette(1024)
    assert len(palette_1) == 1024

    palette_2: bytes = generate_random_palette(768)
    assert len(palette_2) == 768


@pytest.mark.imagetest
def test_get_vga_palette():
    vga_palette: bytes = get_vga_palette()
    assert len(vga_palette) == 768
    assert vga_palette[0] == 0
    assert vga_palette[1] == 0
    assert vga_palette[2] == 0
