"""
Copyright © 2024  Bartłomiej Duda
License: GPL-3.0 License
"""
from enum import Enum

# fmt: off

# Here you can find all image formats supported by ReverseBox

# Legend:
# packed - all channels for single pixel written one next to each other
# planar - each color channel is stored in separate memory block (see "yuv_decoder" for more details")
# bpp - bits per pixel


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
    GRAY8 = "gray8"  # PIX_FMT_GRAY8 / Y, 8bpp  (aliases: Y800 and L8)

    # 16-bit
    GRAY8A = "gray8a"  # PIX_FMT_GRAY8A / 8bit gray, 8bit alpha (LA88)
    GRAY16 = "gray16"  # PIX_FMT_GRAY16LE / PIX_FMT_GRAY16BE / Y, 16bpp
    RGB565 = "rgb565"  # PIX_FMT_RGB565LE / PIX_FMT_RGB565BE / packed RGB 5:6:5, 16bpp
    BGR565 = "bgr565"  # PIX_FMT_BGR565LE / PIX_FMT_BGR565BE / packed BGR 5:6:5, 16bpp
    RGBX5551 = "rgbx5551"
    RGBA5551 = "rgba5551"
    ARGB4444 = "argb4444"
    RGBA4444 = "rgba4444"
    ABGR4444 = "abgr4444"
    RGBX4444 = "rgbx4444"  # PIX_FMT_RGB444LE / PIX_FMT_RGB444BE / packed RGB 4:4:4, 16bpp, alfa bits are ignored (RGB444)
    BGRX4444 = "bgrx4444"  # PIX_FMT_BGR444LE / PIX_FMT_BGR444BE / packed BGR 4:4:4, 16bpp, alfa bits are ignored (BGR444)
    XRGB1555 = "xrgb1555"  # PIX_FMT_RGB555LE / PIX_FMT_RGB555BE / packed RGB 5:5:5, 16bpp, alfa bit is ignored (RGB555)
    XBGR1555 = "xbgr1555"  # PIX_FMT_BGR555LE / PIX_FMT_BGR555BE / packed BGR 5:5:5, 16bpp, alfa bit is ignored (BGR555)
    ARGB1555 = "argb1555"  # TODO - find samples for this
    ABGR1555 = "abgr1555"  # TODO - find samples for this

    # 24-bit
    RGB888 = "rgb888"  # PIX_FMT_RGB24  / packed RGB 8:8:8, 24bpp, RGBRGB
    BGR888 = "bgr888"  # PIX_FMT_BGR24  / packed RGB 8:8:8, 24bpp, BGRBGR

    # 32-bit
    RGBA8888 = "rgba8888"  # PIX_FMT_RGBA / packed RGBA 8:8:8:8, 32bpp, RGBARGBA
    BGRA8888 = "bgra8888"  # PIX_FMT_BGRA / packed BGRA 8:8:8:8, 32bpp, BGRABGRA
    ARGB8888 = "argb8888"  # PIX_FMT_ARGB / packed ARGB 8:8:8:8, 32bpp, ARGBARGB
    ABGR8888 = "abgr8888"  # PIX_FMT_ABGR / packed ABGR 8:8:8:8, 32bpp, ABGRABGR
    XRGB8888 = "xrgb8888"  # PIX_FMT_0RGB / packed RGB 8:8:8, 32bpp, 0RGB0RGB...
    RGBX8888 = "rgbx8888"  # PIX_FMT_RGB0 / packed RGB 8:8:8, 32bpp, RGB0RGB0...
    XBGR8888 = "xbgr8888"  # PIX_FMT_0BGR / packed BGR 8:8:8, 32bpp, 0BGR0BGR...
    BGRX8888 = "bgrx8888"  # PIX_FMT_BGR0 / packed BGR 8:8:8, 32bpp, BGR0BGR0...

    # 48-bit
    RGB48 = "rgb48"  # PIX_FMT_RGB48LE / PIX_FMT_RGB48BE / packed RGB 16:16:16, 48bpp, 16R, 16G, 16B
    BGR48 = "bgr48"  # PIX_FMT_BGR48LE / PIX_FMT_BGR48BE / packed RGB 16:16:16, 48bpp, 16B, 16G, 16R

    # Indexed Formats
    # 4-bit
    PAL4_RGBX5551 = "pal4_rgbx5551"
    PAL4_BGRX5551 = "pal4_bgrx5551"
    PAL4_XRGB1555 = "pal4_xrgb1555"  # RGB555 (little endian)
    PAL4_XBGR1555 = "pal4_xbgr1555"  # BGR555 (little endian)
    PAL4_RGB888 = "pal4_rgb888"
    PAL4_BGR888 = "pal4_bgr888"
    PAL4_RGBA8888 = "pal4_rgba8888"
    PAL4_BGRA8888 = "pal4_bgra8888"
    PAL4_IA8 = "pal4_ia8"  # N64_C4 (type 0)
    PAL4_RGB565 = "pal4_rgb565"  # N64_C4 (type 1)
    PAL4_RGB5A3 = "pal4_rgb5a3"  # N64_C4 (type 2)

    # 8-bit
    PAL8_RGBX2222 = "pal8_rgbx2222"
    PAL8_RGBX5551 = "pal8_rgbx5551"
    PAL8_BGRX5551 = "pal8_bgrx5551"
    PAL8_XRGB1555 = "pal8_xrgb1555"  # RGB555 (little endian)
    PAL8_XBGR1555 = "pal8_xbgr1555"  # BGR555 (little endian)
    PAL8_RGB888 = "pal8_rgb888"
    PAL8_BGR888 = "pal8_bgr888"
    PAL8_RGBX6666 = "pal8_rgbx6666"
    PAL8_IA8 = "pal8_ia8"  # N64_C8 (type 0)
    PAL8_RGB565 = "pal8_rgb565"  # N64_C8 (type 1)
    PAL8_RGB5A3 = "pal8_rgb5a3"  # N64_C8 (type 2)
    PAL8_RGBA8888 = "pal8_rgba8888"
    PAL8_BGRA8888 = "pal8_bgra8888"  # PIX_FMT_PAL8 / 8 bit with PIX_FMT_RGB32 palette

    # 16-bit
    PAL16_IA8 = "pal16_ia8"  # N64_C14X2 (type 0)
    PAL16_RGB565 = "pal16_rgb565"  # N64_C14X2 (type 1)
    PAL16_RGB5A3 = "pal16_rgb5a3"  # N64_C14X2 (type 2)

    # N64 / WII formats
    N64_RGB5A3 = "n64_rgb5a3"  # COLOR+ALPHA, 16bpp
    N64_RGBA32 = "n64_rgba32"  # COLOR+ALPHA, 32bpp
    N64_CMPR = "n64_cmpr"  # COLOR+ALPHA, 4bpp, compressed
    N64_I4 = "n64_i4"  # GRAY, 4bpp
    N64_I8 = "n64_i8"  # GRAY, 8bpp
    N64_IA4 = "n64_ia4"  # GRAY+ALPHA, 8bpp
    N64_IA8 = "n64_ia8"  # GRAY+ALPHA, 16bpp

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
    YUV410P = "yuv410p"  # PIX_FMT_YUV410P / planar YUV 4:1:0, 9bpp, (1 Cr & Cb sample per 4x4 Y samples)
    YUV411P = "yuv411p"  # PIX_FMT_YUV411P / planar YUV 4:1:1, 12bpp, (1 Cr & Cb sample per 4x1 Y samples)
    YUV411_UYYVYY411 = "yuv411_uyyvyy411"  # PIX_FMT_UYYVYY411 / packed YUV 4:1:1, 12bpp, Cb Y0 Y1 Cr Y2 Y3
    YUV420_NV12 = "yuv420_nv12"  # PIX_FMT_NV12 / planar YUV 4:2:0
    YUV420_NV21 = "yuv420_nv21"  # PIX_FMT_NV21 / planar YUV 4:2:0
    YUV420P = "yuv420p"  # PIX_FMT_YUV420P / planar YUV 4:2:0, 12bpp, (1 Cr & Cb sample per 2x2 Y samples)
    YUVA420P = "yuva420p"  # PIX_FMT_YUVA420P / planar YUV 4:2:0, 20bpp, (1 Cr & Cb sample per 2x2 Y & A samples)
    YUV422P = "yuv422p"  # PIX_FMT_YUV422P / planar YUV 4:2:2, 16bpp, (1 Cr & Cb sample per 2x1 Y samples)
    YUV422_UYVY = "yuv422_uyvy"  # PIX_FMT_UYVY422 / packed YUV 4:2:2, 16bpp, Cb Y0 Cr Y1
    YUV422_YUY2 = "yuv422_yuy2"  # PIX_FMT_YUYV422 / packed YUV 4:2:2, 16bpp, Y0 Cb Y1 Cr / <YUY2, YUNV, V422, YUYV>
    YUV440P = "yuv440p"  # PIX_FMT_YUV440P / planar YUV 4:4:0 (1 Cr & Cb sample per 1x2 Y samples)
    YUV444P = "yuv444p"  # PIX_FMT_YUV444P / planar YUV 4:4:4, 24bpp, (1 Cr & Cb sample per 1x1 Y samples)

    # Bumpmaps / Normal maps
    BUMPMAP_SR = "bumpmap_sr"  # 16-bit normal map. Each texel consist of a pair of 8-bit values (S and R)
