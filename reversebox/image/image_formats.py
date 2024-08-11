"""
Copyright © 2024  Bartłomiej Duda
License: GPL-3.0 License
"""
from enum import Enum

# fmt: off


class ImageFormats(Enum):
    # Generic Formats
    # 4-bit
    RGB121 = "rgb121"  # PIX_FMT_RGB4 / packed RGB 1:2:1 bitstream, 4bpp, (msb)1R 2G 1B(lsb)

    # 8-bit
    RGBX2222 = "rgbx2222"
    RGBA2222 = "rgba2222"
    RGB121_BYTE = "rgb121_byte"  # PIX_FMT_RGB4_BYTE / packed RGB 1:2:1, 8bpp, (msb)1R 2G 1B(lsb)
    RGB332 = "rgb332"  # PIX_FMT_RGB8 / packed RGB 3:3:2, 8bpp, (msb)2R 3G 3B(lsb)
    BGR332 = "bgr332"  # PIX_FMT_BGR8 / packed RGB 3:3:2, 8bpp, (msb)2B 3G 3R(lsb)
    GRAY8 = "gray8"  # PIX_FMT_GRAY8 / Y, 8bpp  (same as Y800)

    # 16-bit
    RGB565 = "rgb565"
    BGR565 = "bgr565"
    RGBX5551 = "rgbx5551"
    RGBA5551 = "rgba5551"
    ARGB4444 = "argb4444"
    RGBA4444 = "rgba4444"
    RGBX4444 = "rgbx4444"
    XRGB1555 = "xrgb1555"
    ABGR1555 = "abgr1555"
    XBGR1555 = "xbgr1555"

    # 24-bit
    RGB888 = "rgb888"  # PIX_FMT_RGB24  / packed RGB 8:8:8, 24bpp, RGBRGB
    BGR888 = "bgr888"  # PIX_FMT_BGR24  / packed RGB 8:8:8, 24bpp, BGRBGR

    # 32-bit
    RGBA8888 = "rgba8888"  # PIX_FMT_RGBA / packed RGBA 8:8:8:8, 32bpp, RGBARGBA
    BGRA8888 = "bgra8888"  # PIX_FMT_BGRA / packed BGRA 8:8:8:8, 32bpp, BGRABGRA
    ARGB8888 = "argb8888"  # PIX_FMT_ARGB / packed ARGB 8:8:8:8, 32bpp, ARGBARGB
    ABGR8888 = "abgr8888"  # PIX_FMT_ABGR / packed ABGR 8:8:8:8, 32bpp, ABGRABGR

    # Indexed Formats
    # 4-bit
    PAL4_RGBX5551 = "pal4_rgbx5551"
    PAL4_RGB888 = "pal4_rgb888"
    PAL4_RGBA8888 = "pal4_rgba8888"
    PAL4_IA8 = "pal4_ia8"  # N64_C4 (type 0)
    PAL4_RGB565 = "pal4_rgb565"  # N64_C4 (type 1)
    PAL4_RGB5A3 = "pal4_rgb5a3"  # N64_C4 (type 2)

    # 8-bit
    PAL8_RGBX2222 = "pal8_rgbx2222"
    PAL8_RGBX5551 = "pal8_rgbx5551"
    PAL8_BGRX5551 = "pal8_bgrx5551"
    PAL8_RGB888 = "pal8_rgb888"
    PAL8_BGR888 = "pal8_bgr888"
    PAL8_RGBX6666 = "pal8_rgbx6666"
    PAL8_IA8 = "pal8_ia8"  # N64_C8 (type 0)
    PAL8_RGB565 = "pal8_rgb565"  # N64_C8 (type 1)
    PAL8_RGB5A3 = "pal8_rgb5a3"  # N64_C8 (type 2)
    PAL8_RGBA8888 = "pal8_rgba8888"
    PAL8_BGRA8888 = "pal8_bgra8888"

    # 16-bit
    PAL16_IA8 = "pal16_ia8"  # N64_C14X2 (type 0)
    PAL16_RGB565 = "pal16_rgb565"  # N64_C14X2 (type 1)
    PAL16_RGB5A3 = "pal16_rgb5a3"  # N64_C14X2 (type 2)

    # N64 / WII formats
    N64_RGB5A3 = "n64_rgb5a3"
    N64_I4 = "n64_i4"
    N64_I8 = "n64_i8"
    N64_IA4 = "n64_ia4"
    N64_IA8 = "n64_ia8"

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
    YUY2 = "yuy2"  # PIX_FMT_YUYV422 / packed YUV 4:2:2, 16bpp, Y0 Cb Y1 Cr / <YUY2, YUNV, V422, YUYV>
    NV12 = "nv12"  # PIX_FMT_NV12 / planar YUV 4:2:0
    NV21 = "nv21"  # PIX_FMT_NV21
    UYVY = "uyvy"  # PIX_FMT_UYVY422 / packed YUV 4:2:2, 16bpp, Cb Y0 Cr Y1
    YUV444P = "yuv444p"  # PIX_FMT_YUV444P / planar YUV 4:4:4, 24bpp, (1 Cr & Cb sample per 1x1 Y samples)
    YUV410P = "yuv410p"  # PIX_FMT_YUV410P / planar YUV 4:1:0, 9bpp, (1 Cr & Cb sample per 4x4 Y samples)
    YUV420P = "yuv420p"  # PIX_FMT_YUV420P / planar YUV 4:2:0, 12bpp, (1 Cr & Cb sample per 2x2 Y samples)
    YUV422P = "yuv422p"  # PIX_FMT_YUV422P / planar YUV 4:2:2, 16bpp, (1 Cr & Cb sample per 2x1 Y samples)
    YUV411P = "yuv411p"  # PIX_FMT_YUV411P / planar YUV 4:1:1, 12bpp, (1 Cr & Cb sample per 4x1 Y samples)
    UYYVYY411 = "uyyvyy411"  # PIX_FMT_UYYVYY411 / packed YUV 4:1:1, 12bpp, Cb Y0 Y1 Cr Y2 Y3
    YUV440P = "yuv440p"  # PIX_FMT_YUV440P / planar YUV 4:4:0 (1 Cr & Cb sample per 1x2 Y samples)
    YUVA420P = "yuva420p"  # PIX_FMT_YUVA420P / planar YUV 4:2:0, 20bpp, (1 Cr & Cb sample per 2x2 Y & A samples)
