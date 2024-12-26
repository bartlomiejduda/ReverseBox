"""
Copyright © 2024  Bartłomiej Duda
License: GPL-3.0 License
"""

import pytest

from reversebox.image.common import get_bpp_for_image_format
from reversebox.image.image_formats import ImageFormats

# fmt: off


@pytest.mark.imagetest
def test_common_get_bpp_for_image_format():

    for image_format in ImageFormats:
        bpp: int = get_bpp_for_image_format(image_format)
        assert bpp
        assert bpp > 0
        assert bpp < 100
