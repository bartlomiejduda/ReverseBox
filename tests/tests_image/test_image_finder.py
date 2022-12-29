"""
Copyright © 2022  Bartłomiej Duda
License: GPL-3.0 License
"""

import pytest

from reversebox.image.image_finder_main import run_image_finder


@pytest.mark.imagefinder
def test_image_finder_returns_correct_result():
    image_finder_result = run_image_finder()
    assert image_finder_result == 0
