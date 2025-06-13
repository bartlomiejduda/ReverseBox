"""
Copyright © 2024-2025  Bartłomiej Duda
License: GPL-3.0 License
"""

import pytest

from reversebox.image.common import get_bpp_for_image_format, is_compressed_image_format
from reversebox.image.image_formats import ImageFormats

# fmt: off


@pytest.mark.imagetest
def test_common_get_bpp_for_image_format():
    for image_format in ImageFormats:
        bpp: int = get_bpp_for_image_format(image_format)
        assert bpp
        assert bpp > 0
        assert bpp < 100


@pytest.mark.imagetest
def test_common_is_compressed_image_format():
    for image_format in ImageFormats:
        result: bool = is_compressed_image_format(image_format)

        if image_format in (ImageFormats.BC1_DXT1, ImageFormats.BC2_DXT3, ImageFormats.BC3_DXT5):
            assert result is True

        if image_format in (ImageFormats.RGBA8888, ImageFormats.RGB565):
            assert result is False
