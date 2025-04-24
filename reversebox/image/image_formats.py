"""
Copyright © 2024-2025  Bartłomiej Duda
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
    GRAY8 = "gray8"  # PIX_FMT_GRAY8 / Y, 8bpp  (Y800 / L8 / Luminance 8-bit)
    ALPHA8 = "alpha8"  # (A8 / Alpha 8-bit)
    LA44 = "la44"  # (LA4 / L4A4 / Luminance 4-bit and Alpha 4-bit)
    R8 = "r8"
    G8 = "g8"
    B8 = "b8"

    # 16-bit
    GRAY8A = "gray8a"  # PIX_FMT_GRAY8A / 8bit gray, 8bit alpha (LA88 / LA8 / Luminance 8-bit and Alpha 8-bit)
    GRAY16 = "gray16"  # PIX_FMT_GRAY16LE / PIX_FMT_GRAY16BE / Y, 16bpp
    RG88 = "rg88"  # RG8
    RGB565 = "rgb565"  # PIX_FMT_RGB565LE / PIX_FMT_RGB565BE / packed RGB 5:6:5, 16bpp
    BGR565 = "bgr565"  # PIX_FMT_BGR565LE / PIX_FMT_BGR565BE / packed BGR 5:6:5, 16bpp

    RGBA4444 = "rgba4444"
    RGBX4444 = "rgbx4444"
    BGRA4444 = "bgra4444"
    BGRX4444 = "bgrx4444"

    ARGB4444 = "argb4444"
    XRGB4444 = "xrgb4444"
    ABGR4444 = "abgr4444"
    XBGR4444 = "xbgr4444"

    RGBA5551 = "rgba5551"
    RGBX5551 = "rgbx5551"
    RGBT5551 = "rgbt5551"  # with transparency and tranluciency
    BGRA5551 = "bgra5551"
    BGRX5551 = "bgrx5551"

    ARGB1555 = "argb1555"
    XRGB1555 = "xrgb1555"
    ABGR1555 = "abgr1555"
    XBGR1555 = "xbgr1555"

    R16 = "r16"
    G16 = "g16"
    B16 = "b16"

    # 24-bit
    RGB888 = "rgb888"  # PIX_FMT_RGB24  / packed RGB 8:8:8, 24bpp, RGBRGB
    BGR888 = "bgr888"  # PIX_FMT_BGR24  / packed RGB 8:8:8, 24bpp, BGRBGR

    # 32-bit
    RGBA8888 = "rgba8888"  # PIX_FMT_RGBA / packed RGBA 8:8:8:8, 32bpp, RGBARGBA  (R8G8B8A8_UNORM)
    RGBX8888 = "rgbx8888"  # PIX_FMT_0BGR / packed BGR 8:8:8, 32bpp, 0BGR0BGR...
    BGRA8888 = "bgra8888"  # PIX_FMT_BGRA / packed BGRA 8:8:8:8, 32bpp, BGRABGRA  (B8G8R8A8_UNORM)
    BGRX8888 = "bgrx8888"  # PIX_FMT_BGR0 / packed BGR 8:8:8, 32bpp, BGR0BGR0...  (B8G8R8X8_UNORM)
    ARGB8888 = "argb8888"  # PIX_FMT_ARGB / packed ARGB 8:8:8:8, 32bpp, ARGBARGB
    ABGR8888 = "abgr8888"  # PIX_FMT_ABGR / packed ABGR 8:8:8:8, 32bpp, ABGRABGR
    XRGB8888 = "xrgb8888"  # PIX_FMT_0RGB / packed RGB 8:8:8, 32bpp, 0RGB0RGB...
    RGBM8888 = "rgbm8888"  # (M - brightness multiplier)  TODO - fix this
    R32 = "r32"
    G32 = "g32"
    B32 = "b32"

    # 48-bit
    RGB48 = "rgb48"  # PIX_FMT_RGB48LE / PIX_FMT_RGB48BE / packed RGB 16:16:16, 48bpp, 16R, 16G, 16B
    BGR48 = "bgr48"  # PIX_FMT_BGR48LE / PIX_FMT_BGR48BE / packed RGB 16:16:16, 48bpp, 16B, 16G, 16R

    # Indexed Formats
    PAL4 = "pal4"
    PAL8 = "pal8"
    PAL16 = "pal16"
    PAL_I8A8 = "pal_i8a8"
    PAL32 = "pal32"

    # N64 / WII formats
    N64_RGB5A3 = "n64_rgb5a3"  # COLOR+ALPHA, 16bpp
    N64_RGBA32 = "n64_rgba32"  # COLOR+ALPHA, 32bpp
    N64_CMPR = "n64_cmpr"  # COLOR+ALPHA, 4bpp, compressed
    N64_I4 = "n64_i4"  # GRAY, 4bpp
    N64_I8 = "n64_i8"  # GRAY, 8bpp
    N64_IA4 = "n64_ia4"  # GRAY+ALPHA, 8bpp
    N64_IA8 = "n64_ia8"  # GRAY+ALPHA, 16bpp

    # compressed Formats
    BC1_DXT1 = "bc1_dxt1"
    BC2_DXT3 = "bc2_dxt3"
    BC3_DXT5 = "bc3_dxt5"
    BC4_UNORM = "bc4_unorm"
    BC5_UNORM = "bc5_unorm"
    BC6H_UF16 = "bc6h_uf16"
    BC6H_SF16 = "bc6h_sf16"
    BC7_UNORM = "bc7_unorm"

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
    AYUV = "ayuv"

    # Bumpmaps / Normal maps
    BUMPMAP_SR = "bumpmap_sr"  # 16-bit normal map. Each texel consist of a pair of 8-bit values (S and R)
