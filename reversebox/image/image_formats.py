"""
Copyright © 2024  Bartłomiej Duda
License: GPL-3.0 License
"""
from enum import Enum


class ImageFormats(Enum):
    RGBX2222 = "rgbx2222"
    RGBA2222 = "rgba2222"
    RGB565 = "rgb565"
    RGB888 = "rgb888"
    BGR888 = "bgr888"
    ARGB4444 = "argb4444"
    RGBA4444 = "rgba4444"
    XRGB1555 = "xrgb1555"
    ABGR1555 = "abgr1555"
    XBGR1555 = "xbgr1555"
    ARGB8888 = "argb8888"

    PAL4_RGBX5551 = "pal4_rgbx5551"
    PAL4_RGB888 = "pal4_rgb888"
    PAL4_RGBA8888 = "pal4_rgba8888"
    PAL8_RGBX5551 = "pal8_rgbx5551"
    PAL8_RGB888 = "pal8_rgb888"
    PAL8_RGBA8888 = "pal8_rgba8888"

    DXT1 = "dxt1"
    DXT3 = "dxt3"
