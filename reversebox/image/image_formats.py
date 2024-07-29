"""
Copyright © 2024  Bartłomiej Duda
License: GPL-3.0 License
"""
from enum import Enum


class ImageFormats(Enum):
    # Generic Formats
    RGBX2222 = "rgbx2222"
    RGBA2222 = "rgba2222"
    RGB565 = "rgb565"
    BGR565 = "bgr565"
    RGBX5551 = "rgbx5551"
    RGBA5551 = "rgba5551"
    RGB888 = "rgb888"
    BGR888 = "bgr888"
    ARGB4444 = "argb4444"
    RGBA4444 = "rgba4444"
    RGBX4444 = "rgbx4444"
    XRGB1555 = "xrgb1555"
    ABGR1555 = "abgr1555"
    XBGR1555 = "xbgr1555"
    ARGB8888 = "argb8888"
    ABGR8888 = "abgr8888"
    RGBA8888 = "rgba8888"

    # Indexed Formats
    PAL4_RGBX5551 = "pal4_rgbx5551"
    PAL4_RGB888 = "pal4_rgb888"
    PAL4_RGB565 = "pal4_rgb565"
    PAL4_RGBA8888 = "pal4_rgba8888"
    PAL4_RGB5A3 = "pal4_rgb5a3"
    PAL8_RGBX2222 = "pal8_rgbx2222"
    PAL8_RGBX5551 = "pal8_rgbx5551"
    PAL8_BGRX5551 = "pal8_bgrx5551"
    PAL8_RGB888 = "pal8_rgb888"
    PAL8_BGR888 = "pal8_bgr888"
    PAL8_RGB565 = "pal8_rgb565"
    PAL8_RGBX6666 = "pal8_rgbx6666"
    PAL8_RGB5A3 = "pal8_rgb5a3"
    PAL8_RGBA8888 = "pal8_rgba8888"
    PAL8_BGRA8888 = "pal8_bgra8888"

    # N64 / WII formats
    N64_RGB5A3 = "n64_rgb5a3"

    # DXT Formats
    DXT1 = "dxt1"  # BC1
    DXT3 = "dxt3"  # BC2
    DXT5 = "dxt5"  # BC3

    # PS2 GS Texture Formats
    GST121 = "gst121"
    GST221 = "gst221"
    GST421 = "gst421"
    GST821 = "gst821"
    GST122 = "gst122"
    GST222 = "gst222"
    GST422 = "gst422"
    GST822 = "gst822"

    # YUV Formats
    # https://wiki.videolan.org/YUV
    # https://gstreamer.freedesktop.org/documentation/additional/design/mediatype-video-raw.html
    # https://web.archive.org/web/20190220164028/http://www.sunrayimage.com/examples.html
    # Example: ffmpeg -i <input file path> -vf format=yuv240p -frames:v 1 output_image.yuv
    YUY2 = "yuy2"  # packed 4:2:2 YUV  /  |Y0|U0|Y1|V0|
    MADYUV = "madyuv"  # TODO - same as YUY2? Needs more research...
