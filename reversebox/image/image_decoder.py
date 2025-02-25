"""
Copyright © 2024-2025  Bartłomiej Duda
License: GPL-3.0 License
"""

import struct

from reversebox.common.logger import get_logger
from reversebox.image.decoders.bumpmap_decoder import BumpmapDecoder
from reversebox.image.decoders.compressed_decoder import CompressedImageDecoder
from reversebox.image.decoders.gst_decoder import GSTImageDecoder
from reversebox.image.decoders.n64_decoder import N64Decoder
from reversebox.image.decoders.yuv_decoder import YUVDecoder
from reversebox.image.image_formats import ImageFormats
from reversebox.image.pillow_wrapper import PillowWrapper
from reversebox.io_files.bytes_handler import BytesHandler
from reversebox.io_files.bytes_helper_functions import (
    get_uint8,
    get_uint16,
    get_uint24,
    get_uint32,
    get_uint48,
)

logger = get_logger(__name__)

# fmt: off
# mypy: ignore-errors


class ImageDecoder:

    pillow_wrapper = PillowWrapper()

    def __init__(self):
        pass

    def _decode_rgb121_byte_pixel(self, pixel_int: int) -> bytes:
        p = bytearray(4)
        p[0] = (pixel_int >> 3) * 255
        p[1] = ((pixel_int >> 1) & 3) * 85
        p[2] = (pixel_int & 1) * 255
        p[3] = 0xFF
        return p

    def _decode_rgbx2222_pixel(self, pixel_int: int) -> bytes:
        p = bytearray(4)
        p[0] = (pixel_int & 3) * 85
        p[1] = ((pixel_int >> 2) & 3) * 85
        p[2] = ((pixel_int >> 4) & 3) * 85
        p[3] = 0xFF
        return p

    def _decode_rgba2222_pixel(self, pixel_int: int) -> bytes:
        p = bytearray(4)
        p[0] = (pixel_int & 3) * 85
        p[1] = ((pixel_int >> 2) & 3) * 85
        p[2] = ((pixel_int >> 4) & 3) * 85
        p[3] = ((pixel_int >> 6) & 3) * 85
        return p

    def _decode_gray8_pixel(self, pixel_int: int) -> bytes:
        p = bytearray(4)
        p[0] = pixel_int & 255
        p[1] = pixel_int & 255
        p[2] = pixel_int & 255
        p[3] = 0xFF
        return p

    def _decode_gray8a_pixel(self, pixel_int: int) -> bytes:
        p = bytearray(4)
        L = pixel_int & 0xFF
        A = (pixel_int >> 8) & 0xFF
        p[0] = L
        p[1] = L
        p[2] = L
        p[3] = A
        return p

    def _decode_gray16_pixel(self, pixel_int: int) -> bytes:
        p = bytearray(4)
        L = pixel_int & 0xFFFF
        L = L >> 8
        p[0] = L
        p[1] = L
        p[2] = L
        p[3] = 0xFF
        return p

    def _decode_rgb332_pixel(self, pixel_int: int) -> bytes:
        p = bytearray(4)
        p[0] = (pixel_int >> 5) * 36
        p[1] = ((pixel_int >> 2) & 7) * 36
        p[2] = (pixel_int & 3) * 85
        p[3] = 0xFF
        return p

    def _decode_bgr332_pixel(self, pixel_int: int) -> bytes:
        p = bytearray(4)
        p[0] = (pixel_int & 7) * 36
        p[1] = ((pixel_int >> 3) & 7) * 36
        p[2] = (pixel_int >> 6) * 85
        p[3] = 0xFF
        return p

    def _decode_bgrx5551_pixel(self, pixel_int: int) -> bytes:
        p = bytearray(4)
        b = pixel_int & 0x1F
        g = (pixel_int >> 5) & 0x1F
        r = (pixel_int >> 10) & 0x1F
        p[0] = (r << 3) | (r >> 2)
        p[1] = (g << 3) | (g >> 2)
        p[2] = (b << 3) | (b >> 2)
        p[3] = 0xFF
        return p

    def _decode_bgra5551_pixel(self, pixel_int: int) -> bytes:
        p = bytearray(4)
        b = pixel_int & 0x1F
        g = (pixel_int >> 5) & 0x1F
        r = (pixel_int >> 10) & 0x1F
        a = (pixel_int >> 15) & 0x1
        p[0] = (r << 3) | (r >> 2)
        p[1] = (g << 3) | (g >> 2)
        p[2] = (b << 3) | (b >> 2)
        p[3] = (0x00 if a == 0 else 0xFF)
        return p

    def _decode_rgbx5551_pixel(self, pixel_int: int) -> bytes:
        p = bytearray(4)
        r = pixel_int & 0x1F
        g = (pixel_int >> 5) & 0x1F
        b = (pixel_int >> 10) & 0x1F
        p[0] = (r << 3) | (r >> 2)
        p[1] = (g << 3) | (g >> 2)
        p[2] = (b << 3) | (b >> 2)
        p[3] = 0xFF
        return p

    def _decode_rgba5551_pixel(self, pixel_int: int) -> bytes:
        p = bytearray(4)
        r = pixel_int & 0x1F
        g = (pixel_int >> 5) & 0x1F
        b = (pixel_int >> 10) & 0x1F
        a = (pixel_int >> 15) & 0x1
        p[0] = (r << 3) | (r >> 2)
        p[1] = (g << 3) | (g >> 2)
        p[2] = (b << 3) | (b >> 2)
        p[3] = (0x00 if a == 0 else 0xFF)
        return p

    def _decode_xrgb1555_pixel(self, pixel_int: int) -> bytes:
        p = bytearray(4)
        p[0] = (((pixel_int >> 1) & 0x1F) * 0xFF // 0x1F)
        p[1] = (((pixel_int >> 6) & 0x1F) * 0xFF // 0x1F)
        p[2] = (((pixel_int >> 11) & 0x1F) * 0xFF // 0x1F)
        p[3] = 0xFF
        return p

    def _decode_argb1555_pixel(self, pixel_int: int) -> bytes:
        p = bytearray(4)
        a = (((pixel_int >> 0) & 0x01) * 0xFF // 0x1F)
        p[0] = (((pixel_int >> 1) & 0x1F) * 0xFF // 0x1F)
        p[1] = (((pixel_int >> 6) & 0x1F) * 0xFF // 0x1F)
        p[2] = (((pixel_int >> 11) & 0x1F) * 0xFF // 0x1F)
        p[3] = 0xFF if a else 0x00
        return p

    def _decode_xbgr1555_pixel(self, pixel_int: int) -> bytes:
        p = bytearray(4)
        p[0] = (((pixel_int >> 11) & 0x1F) * 0xFF // 0x1F)
        p[1] = (((pixel_int >> 6) & 0x1F) * 0xFF // 0x1F)
        p[2] = (((pixel_int >> 1) & 0x1F) * 0xFF // 0x1F)
        p[3] = 0xFF
        return p

    def _decode_abgr1555_pixel(self, pixel_int: int) -> bytes:
        p = bytearray(4)
        a = (((pixel_int >> 0) & 0x01) * 0xFF // 0x1F)
        p[0] = (((pixel_int >> 11) & 0x1F) * 0xFF // 0x1F)
        p[1] = (((pixel_int >> 6) & 0x1F) * 0xFF // 0x1F)
        p[2] = (((pixel_int >> 1) & 0x1F) * 0xFF // 0x1F)
        p[3] = 0xFF if a else 0x00
        return p

    def _decode_bgr565_pixel(self, pixel_int: int) -> bytes:
        p = bytearray(4)
        p[0] = ((pixel_int >> 11) & 0x1F) * 0xFF // 0x1F
        p[1] = ((pixel_int >> 5) & 0x3F) * 0xFF // 0x3F
        p[2] = ((pixel_int >> 0) & 0x1F) * 0xFF // 0x1F
        p[3] = 0xFF
        return p

    def _decode_rgb565_pixel(self, pixel_int: int) -> bytes:
        p = bytearray(4)
        p[0] = ((pixel_int >> 0) & 0x1F) * 0xFF // 0x1F
        p[1] = ((pixel_int >> 5) & 0x3F) * 0xFF // 0x3F
        p[2] = ((pixel_int >> 11) & 0x1F) * 0xFF // 0x1F
        p[3] = 0xFF
        return p

    def _decode_rgb5A3_pixel(self, pixel_int: int) -> bytes:
        p = bytearray(4)
        if pixel_int & 0x8000:  # rgb555
            p[0] = (((pixel_int >> 10) & 0x1F) * 0xFF // 0x1F)
            p[1] = (((pixel_int >> 5) & 0x1F) * 0xFF // 0x1F)
            p[2] = (((pixel_int >> 0) & 0x1F) * 0xFF // 0x1F)
            p[3] = 0xFF
        else:  # argb3444
            p[0] = (((pixel_int >> 8) & 0x0F) * 0xFF // 0x0F)
            p[1] = (((pixel_int >> 4) & 0x0F) * 0xFF // 0x0F)
            p[2] = (((pixel_int >> 0) & 0x0F) * 0xFF // 0x0F)
            p[3] = (((pixel_int >> 12) & 0x07) * 0xFF // 0x07)
        return p

    def _decode_rgb888_pixel(self, pixel_int: int) -> bytes:
        p = bytearray(4)
        p[0] = (pixel_int >> 0) & 0xff
        p[1] = (pixel_int >> 8) & 0xff
        p[2] = (pixel_int >> 16) & 0xff
        p[3] = 0xFF
        return p

    def _decode_bgr888_pixel(self, pixel_int: int) -> bytes:
        p = bytearray(4)
        p[0] = (pixel_int >> 16) & 0xff
        p[1] = (pixel_int >> 8) & 0xff
        p[2] = (pixel_int >> 0) & 0xff
        p[3] = 0xFF
        return p

    def _decode_rgba8888_pixel(self, pixel_int: int) -> bytes:
        p = bytearray(4)
        p[0] = (pixel_int >> 0) & 0xff
        p[1] = (pixel_int >> 8) & 0xff
        p[2] = (pixel_int >> 16) & 0xff
        p[3] = (pixel_int >> 24) & 0xff
        return p

    def _decode_bgrx8888_pixel(self, pixel_int: int) -> bytes:
        p = bytearray(4)
        p[0] = (pixel_int >> 16) & 0xFF
        p[1] = (pixel_int >> 8) & 0xFF
        p[2] = (pixel_int >> 0) & 0xFF
        p[3] = 0xFF
        return p

    # TODO - fix this, not decoding properly
    def _decode_rgbm8888_pixel(self, pixel_int: int) -> bytes:
        p = bytearray(4)
        max_range = 65025
        r = (pixel_int >> 0) & 0xFF
        g = (pixel_int >> 8) & 0xFF
        b = (pixel_int >> 16) & 0xFF
        m = (pixel_int >> 24) & 0xFF

        r_normalized = r / 255.0
        g_normalized = g / 255.0
        b_normalized = b / 255.0
        m_normalized = m / 255.0

        r_final = int(r_normalized * (m_normalized * max_range) * 255)
        g_final = int(g_normalized * (m_normalized * max_range) * 255)
        b_final = int(b_normalized * (m_normalized * max_range) * 255)

        p[0] = min(max(r_final, 0), 255)
        p[1] = min(max(g_final, 0), 255)
        p[2] = min(max(b_final, 0), 255)
        p[3] = 0xFF
        return p

    def _decode_bgra8888_pixel(self, pixel_int: int) -> bytes:
        p = bytearray(4)
        p[0] = (pixel_int >> 16) & 0xff
        p[1] = (pixel_int >> 8) & 0xff
        p[2] = (pixel_int >> 0) & 0xff
        p[3] = (pixel_int >> 24) & 0xff
        return p

    def _decode_abgr8888_pixel(self, pixel_int: int) -> bytes:
        p = bytearray(4)
        p[0] = (pixel_int >> 24) & 0xff
        p[1] = (pixel_int >> 16) & 0xff
        p[2] = (pixel_int >> 8) & 0xff
        p[3] = (pixel_int >> 0) & 0xff
        return p

    def _decode_argb8888_pixel(self, pixel_int: int) -> bytes:
        p = bytearray(4)
        p[0] = (pixel_int >> 8) & 0xff
        p[1] = (pixel_int >> 16) & 0xff
        p[2] = (pixel_int >> 24) & 0xff
        p[3] = (pixel_int >> 0) & 0xff
        return p

    def _decode_xrgb8888_pixel(self, pixel_int: int) -> bytes:
        p = bytearray(4)
        p[0] = (pixel_int >> 8) & 0xff
        p[1] = (pixel_int >> 16) & 0xff
        p[2] = (pixel_int >> 24) & 0xff
        p[3] = 0xFF
        return p

    def _decode_rgbx8888_pixel(self, pixel_int: int) -> bytes:
        p = bytearray(4)
        p[0] = (pixel_int >> 0) & 0xFF
        p[1] = (pixel_int >> 8) & 0xFF
        p[2] = (pixel_int >> 16) & 0xFF
        p[3] = 0xFF
        return p

    def _decode_xrgb4444_pixel(self, pixel_int: int) -> bytes:
        p = bytearray(4)
        r = (pixel_int >> 4) & 0x0f
        g = (pixel_int >> 8) & 0x0f
        b = (pixel_int >> 12) & 0xff
        p[0] = (r << 4) | (r >> 0)
        p[1] = (g << 4) | (g >> 0)
        p[2] = (b << 4) | (b >> 0)
        p[3] = 0xFF
        return p

    def _decode_argb4444_pixel(self, pixel_int: int) -> bytes:
        p = bytearray(4)
        a = (pixel_int >> 0) & 0x0f
        r = (pixel_int >> 4) & 0x0f
        g = (pixel_int >> 8) & 0x0f
        b = (pixel_int >> 12) & 0xff
        p[0] = (r << 4) | (r >> 0)
        p[1] = (g << 4) | (g >> 0)
        p[2] = (b << 4) | (b >> 0)
        p[3] = (a << 4) | (a >> 0)
        return p

    def _decode_xbgr4444_pixel(self, pixel_int: int) -> bytes:
        p = bytearray(4)
        b = (pixel_int >> 4) & 0x0f
        g = (pixel_int >> 8) & 0x0f
        r = (pixel_int >> 12) & 0xff
        p[0] = (r << 4) | (r >> 0)
        p[1] = (g << 4) | (g >> 0)
        p[2] = (b << 4) | (b >> 0)
        p[3] = 0xFF
        return p

    def _decode_abgr4444_pixel(self, pixel_int: int) -> bytes:
        p = bytearray(4)
        a = (pixel_int >> 0) & 0x0f
        b = (pixel_int >> 4) & 0x0f
        g = (pixel_int >> 8) & 0x0f
        r = (pixel_int >> 12) & 0xff
        p[0] = (r << 4) | (r >> 0)
        p[1] = (g << 4) | (g >> 0)
        p[2] = (b << 4) | (b >> 0)
        p[3] = (a << 4) | (a >> 0)
        return p

    def _decode_bgrx4444_pixel(self, pixel_int: int) -> bytes:
        p = bytearray(4)
        b = (pixel_int >> 0) & 0x0f
        g = (pixel_int >> 4) & 0x0f
        r = (pixel_int >> 8) & 0x0f
        p[0] = (r << 4) | (r >> 0)
        p[1] = (g << 4) | (g >> 0)
        p[2] = (b << 4) | (b >> 0)
        p[3] = 0xFF
        return p

    def _decode_bgra4444_pixel(self, pixel_int: int) -> bytes:
        p = bytearray(4)
        b = (pixel_int >> 0) & 0x0f
        g = (pixel_int >> 4) & 0x0f
        r = (pixel_int >> 8) & 0x0f
        a = (pixel_int >> 12) & 0xff
        p[0] = (r << 4) | (r >> 0)
        p[1] = (g << 4) | (g >> 0)
        p[2] = (b << 4) | (b >> 0)
        p[3] = (a << 4) | (a >> 0)
        return p

    def _decode_rgbx4444_pixel(self, pixel_int: int) -> bytes:
        p = bytearray(4)
        r = (pixel_int >> 0) & 0x0f
        g = (pixel_int >> 4) & 0x0f
        b = (pixel_int >> 8) & 0x0f
        p[0] = (r << 4) | (r >> 0)
        p[1] = (g << 4) | (g >> 0)
        p[2] = (b << 4) | (b >> 0)
        p[3] = 0xFF
        return p

    def _decode_rgba4444_pixel(self, pixel_int: int) -> bytes:
        p = bytearray(4)
        r = (pixel_int >> 0) & 0x0f
        g = (pixel_int >> 4) & 0x0f
        b = (pixel_int >> 8) & 0x0f
        a = (pixel_int >> 12) & 0x0f
        p[0] = (r << 4) | (r >> 0)
        p[1] = (g << 4) | (g >> 0)
        p[2] = (b << 4) | (b >> 0)
        p[3] = (a << 4) | (a >> 0)
        return p

    def _decode_rgbx6666_pixel(self, pixel_int: int) -> bytes:
        p = bytearray(4)
        p[0] = (((pixel_int >> 0) & 63) * 255 + 32) // 63
        p[1] = (((pixel_int >> 8) & 63) * 255 + 32) // 63
        p[2] = (((pixel_int >> 16) & 63) * 255 + 32) // 63
        p[3] = 0xFF
        return p

    def _decode_rgb48_pixel(self, pixel_int: int) -> bytes:
        p = bytearray(4)
        r = (pixel_int & 0xFFFF)
        g = (pixel_int >> 16) & 0xFFFF
        b = (pixel_int >> 32) & 0xFFFF
        r_8bit = (r >> 8) & 0xFF
        g_8bit = (g >> 8) & 0xFF
        b_8bit = (b >> 8) & 0xFF
        p[0] = r_8bit
        p[1] = g_8bit
        p[2] = b_8bit
        p[3] = 0xFF
        return p

    def _decode_bgr48_pixel(self, pixel_int: int) -> bytes:
        p = bytearray(4)
        b = (pixel_int & 0xFFFF)
        g = (pixel_int >> 16) & 0xFFFF
        r = (pixel_int >> 32) & 0xFFFF
        r_8bit = (r >> 8) & 0xFF
        g_8bit = (g >> 8) & 0xFF
        b_8bit = (b >> 8) & 0xFF
        p[0] = r_8bit
        p[1] = g_8bit
        p[2] = b_8bit
        p[3] = 0xFF
        return p

    def _decode_i4_pixel(self, pixel_int: int) -> bytes:
        p = bytearray(4)
        p[0] = pixel_int * 0x11
        p[1] = pixel_int * 0x11
        p[2] = pixel_int * 0x11
        p[3] = 0xFF
        return p

    def _decode_i8_pixel(self, pixel_int: int) -> bytes:
        p = bytearray(4)
        p[0] = pixel_int
        p[1] = pixel_int
        p[2] = pixel_int
        p[3] = 0xFF
        return p

    def _decode_ia4_pixel(self, pixel_int: int) -> bytes:
        p = bytearray(4)
        p[0] = (pixel_int & 0xF) * 0x11
        p[1] = (pixel_int & 0xF) * 0x11
        p[2] = (pixel_int & 0xF) * 0x11
        p[3] = (pixel_int >> 4) * 0x11
        return p

    def _decode_ia8_pixel(self, pixel_int: int) -> bytes:
        p = bytearray(4)
        p[0] = pixel_int & 0xFF
        p[1] = pixel_int & 0xFF
        p[2] = pixel_int & 0xFF
        p[3] = pixel_int >> 8
        return p

    def _decode_r_only_pixel(self, pixel_int: int) -> bytes:
        p = bytearray(4)
        p[0] = pixel_int & 0xFF
        p[1] = 0x00
        p[2] = 0x00
        p[3] = 0xFF
        return p

    def _decode_g_only_pixel(self, pixel_int: int) -> bytes:
        p = bytearray(4)
        p[0] = 0x00
        p[1] = pixel_int & 0xFF
        p[2] = 0x00
        p[3] = 0xFF
        return p

    def _decode_b_only_pixel(self, pixel_int: int) -> bytes:
        p = bytearray(4)
        p[0] = 0x00
        p[1] = 0x00
        p[2] = pixel_int & 0xFF
        p[3] = 0xFF
        return p

    # source format is one of the listed below
    # target format is always RGBA8888
    generic_data_formats = {
        # image_format: (decode_function, bits_per_pixel, image_entry_read_function)
        ImageFormats.RGB121: (_decode_rgb121_byte_pixel, 4, get_uint8),
        ImageFormats.N64_I4: (_decode_i4_pixel, 4, get_uint8),  # GRAY, 4bpp

        ImageFormats.RGB121_BYTE: (_decode_rgb121_byte_pixel, 8, get_uint8),
        ImageFormats.GRAY8: (_decode_gray8_pixel, 8, get_uint8),
        ImageFormats.RGBX2222: (_decode_rgbx2222_pixel, 8, get_uint8),
        ImageFormats.RGBA2222: (_decode_rgba2222_pixel, 8, get_uint8),
        ImageFormats.RGB332: (_decode_rgb332_pixel, 8, get_uint8),
        ImageFormats.BGR332: (_decode_bgr332_pixel, 8, get_uint8),
        ImageFormats.N64_I8: (_decode_i8_pixel, 8, get_uint8),  # GRAY, 8bpp
        ImageFormats.N64_IA4: (_decode_ia4_pixel, 8, get_uint8),  # GRAY+ALPHA, 8bpp
        ImageFormats.R8: (_decode_r_only_pixel, 8, get_uint8),
        ImageFormats.G8: (_decode_g_only_pixel, 8, get_uint8),
        ImageFormats.B8: (_decode_b_only_pixel, 8, get_uint8),

        ImageFormats.GRAY8A: (_decode_gray8a_pixel, 16, get_uint16),
        ImageFormats.GRAY16: (_decode_gray16_pixel, 16, get_uint16),
        ImageFormats.RGB565: (_decode_rgb565_pixel, 16, get_uint16),
        ImageFormats.BGR565: (_decode_bgr565_pixel, 16, get_uint16),
        ImageFormats.RGBX5551: (_decode_rgbx5551_pixel, 16, get_uint16),
        ImageFormats.RGBA5551: (_decode_rgba5551_pixel, 16, get_uint16),
        ImageFormats.BGRA5551: (_decode_bgra5551_pixel, 16, get_uint16),
        ImageFormats.BGRX5551: (_decode_bgrx5551_pixel, 16, get_uint16),
        ImageFormats.RGBA4444: (_decode_rgba4444_pixel, 16, get_uint16),
        ImageFormats.ARGB4444: (_decode_argb4444_pixel, 16, get_uint16),
        ImageFormats.XRGB4444: (_decode_xrgb4444_pixel, 16, get_uint16),
        ImageFormats.ABGR4444: (_decode_abgr4444_pixel, 16, get_uint16),
        ImageFormats.XBGR4444: (_decode_xbgr4444_pixel, 16, get_uint16),
        ImageFormats.RGBX4444: (_decode_rgbx4444_pixel, 16, get_uint16),  # RGB444
        ImageFormats.BGRA4444: (_decode_bgra4444_pixel, 16, get_uint16),  # BGR444
        ImageFormats.BGRX4444: (_decode_bgrx4444_pixel, 16, get_uint16),  # BGR444
        ImageFormats.XRGB1555: (_decode_xrgb1555_pixel, 16, get_uint16),  # RGB555
        ImageFormats.XBGR1555: (_decode_xbgr1555_pixel, 16, get_uint16),  # BGR555
        ImageFormats.ARGB1555: (_decode_argb1555_pixel, 16, get_uint16),
        ImageFormats.ABGR1555: (_decode_abgr1555_pixel, 16, get_uint16),
        ImageFormats.N64_IA8: (_decode_ia8_pixel, 16, get_uint16),  # GRAY+ALPHA, 16bpp
        ImageFormats.N64_RGB5A3: (_decode_rgb5A3_pixel, 16, get_uint16),
        ImageFormats.R16: (_decode_r_only_pixel, 16, get_uint16),
        ImageFormats.G16: (_decode_g_only_pixel, 16, get_uint16),
        ImageFormats.B16: (_decode_b_only_pixel, 16, get_uint16),

        ImageFormats.RGB888: (_decode_rgb888_pixel, 24, get_uint24),
        ImageFormats.BGR888: (_decode_bgr888_pixel, 24, get_uint24),

        ImageFormats.ARGB8888: (_decode_argb8888_pixel, 32, get_uint32),
        ImageFormats.ABGR8888: (_decode_abgr8888_pixel, 32, get_uint32),
        ImageFormats.RGBA8888: (_decode_rgba8888_pixel, 32, get_uint32),
        ImageFormats.BGRA8888: (_decode_bgra8888_pixel, 32, get_uint32),
        ImageFormats.XRGB8888: (_decode_xrgb8888_pixel, 32, get_uint32),
        ImageFormats.RGBX8888: (_decode_rgbx8888_pixel, 32, get_uint32),
        ImageFormats.BGRX8888: (_decode_bgrx8888_pixel, 32, get_uint32),
        ImageFormats.RGBM8888: (_decode_rgbm8888_pixel, 32, get_uint32),
        ImageFormats.R32: (_decode_r_only_pixel, 32, get_uint32),
        ImageFormats.G32: (_decode_g_only_pixel, 32, get_uint32),
        ImageFormats.B32: (_decode_b_only_pixel, 32, get_uint32),

        ImageFormats.RGB48: (_decode_rgb48_pixel, 48, get_uint48),
        ImageFormats.BGR48: (_decode_bgr48_pixel, 48, get_uint48),
    }

    indexed_data_formats = {
        # image_format: (decode_function, bits_per_pixel, palette_entry_size, palette_entry_read_function)
        ImageFormats.PAL4_RGBX5551: (_decode_rgbx5551_pixel, 4, 2, get_uint16),
        ImageFormats.PAL4_BGRX5551: (_decode_bgrx5551_pixel, 4, 2, get_uint16),
        ImageFormats.PAL4_XRGB1555: (_decode_xrgb1555_pixel, 4, 2, get_uint16),  # RGB555 (little endian)
        ImageFormats.PAL4_XBGR1555: (_decode_xbgr1555_pixel, 4, 2, get_uint16),  # BGR555 (little endian)
        ImageFormats.PAL4_RGB888: (_decode_rgb888_pixel, 4, 3, get_uint24),
        ImageFormats.PAL4_BGR888: (_decode_bgr888_pixel, 4, 3, get_uint24),
        ImageFormats.PAL4_RGBA8888: (_decode_rgba8888_pixel, 4, 4, get_uint32),
        ImageFormats.PAL4_BGRA8888: (_decode_bgra8888_pixel, 4, 4, get_uint32),
        ImageFormats.PAL4_IA8: (_decode_ia8_pixel, 4, 2, get_uint16),  # N64_C4 (type 0)
        ImageFormats.PAL4_RGB565: (_decode_rgb565_pixel, 4, 2, get_uint16),  # N64_C4 (type 1)
        ImageFormats.PAL4_RGB5A3: (_decode_rgb5A3_pixel, 4, 2, get_uint16),  # N64_C4 (type 2)
        ImageFormats.PAL4_GRAY8: (_decode_gray8_pixel, 4, 1, get_uint8),

        ImageFormats.PAL8_RGBX2222: (_decode_rgbx2222_pixel, 8, 1, get_uint8),
        ImageFormats.PAL8_RGBX5551: (_decode_rgbx5551_pixel, 8, 2, get_uint16),
        ImageFormats.PAL8_BGRX5551: (_decode_bgrx5551_pixel, 8, 2, get_uint16),
        ImageFormats.PAL8_XRGB1555: (_decode_xrgb1555_pixel, 8, 2, get_uint16),  # RGB555 (little endian)
        ImageFormats.PAL8_XBGR1555: (_decode_xbgr1555_pixel, 8, 2, get_uint16),  # BGR555 (little endian)
        ImageFormats.PAL8_RGB888: (_decode_rgb888_pixel, 8, 3, get_uint24),
        ImageFormats.PAL8_BGR888: (_decode_bgr888_pixel, 8, 3, get_uint24),
        ImageFormats.PAL8_RGBX6666: (_decode_rgbx6666_pixel, 8, 3, get_uint24),
        ImageFormats.PAL8_IA8: (_decode_ia8_pixel, 8, 2, get_uint16),  # N64_C8 (type 0)
        ImageFormats.PAL8_RGB565: (_decode_rgb565_pixel, 8, 2, get_uint16),  # N64_C8 (type 1)
        ImageFormats.PAL8_RGB5A3: (_decode_rgb5A3_pixel, 8, 2, get_uint16),  # N64_C8 (type 2)
        ImageFormats.PAL8_RGBA8888: (_decode_rgba8888_pixel, 8, 4, get_uint32),
        ImageFormats.PAL8_BGRA8888: (_decode_bgra8888_pixel, 8, 4, get_uint32),
        ImageFormats.PAL8_GRAY8: (_decode_gray8_pixel, 8, 1, get_uint8),

        ImageFormats.PAL16_IA8: (_decode_ia8_pixel, 16, 2, get_uint16),  # N64_C14X2 (type 0)
        ImageFormats.PAL16_RGB565: (_decode_rgb565_pixel, 16, 2, get_uint16),  # N64_C14X2 (type 1)
        ImageFormats.PAL16_RGB5A3: (_decode_rgb5A3_pixel, 16, 2, get_uint16),  # N64_C14X2 (type 2)
        ImageFormats.PAL16_RGBA8888: (_decode_rgba8888_pixel, 16, 2, get_uint16),
        ImageFormats.PAL_I8A8_BGRA8888: (_decode_bgra8888_pixel, 16, 4, get_uint32),
    }

    def _get_endianess_format(self, endianess: str) -> str:
        if endianess == "little":
            endianess_format = "<"
        elif endianess == "big":
            endianess_format = ">"
        else:
            raise Exception("Wrong endianess!")
        return endianess_format

    def _decode_generic(self, image_data: bytes, img_width: int, img_height: int, image_format: tuple, image_endianess: str) -> bytes:
        decode_function, bits_per_pixel, image_entry_read_function = image_format
        image_handler = BytesHandler(image_data)
        texture_data = bytearray(img_width * img_height * 4)
        read_offset = 0
        image_endianess_format: str = self._get_endianess_format(image_endianess)

        if bits_per_pixel == 4:
            for i in range(0, img_width * img_height, 2):
                image_pixel: bytes = image_handler.get_bytes(read_offset, 1)
                pixel_int: int = image_entry_read_function(image_pixel, image_endianess_format)
                if image_endianess == "little":
                    texture_data[i * 4:(i + 1) * 4] = decode_function(self, pixel_int & 0xf)  # noqa
                    texture_data[(i + 1) * 4:(i + 2) * 4] = decode_function(self, (pixel_int >> 4) & 0xf)  # noqa
                elif image_endianess == "big":
                    texture_data[i * 4:(i + 1) * 4] = decode_function(self, (pixel_int >> 4) & 0xf)  # noqa
                    texture_data[(i + 1) * 4:(i + 2) * 4] = decode_function(self, pixel_int & 0xf)  # noqa
                else:
                    raise Exception(f"Endianess not supported! Endianess: {image_endianess}")
                read_offset += 1
        elif bits_per_pixel == 8:
            bytes_per_pixel = 1
            for i in range(len(image_data) // bytes_per_pixel):
                image_pixel: bytes = image_handler.get_bytes(read_offset, bytes_per_pixel)
                pixel_int: int = image_entry_read_function(image_pixel, image_endianess_format)
                read_offset += bytes_per_pixel
                texture_data[i * 4 : (i + 1) * 4] = decode_function(self, pixel_int)  # noqa
        elif bits_per_pixel == 16:
            bytes_per_pixel = 2
            for i in range(len(image_data) // bytes_per_pixel):
                image_pixel: bytes = image_handler.get_bytes(read_offset, bytes_per_pixel)
                pixel_int: int = image_entry_read_function(image_pixel, image_endianess_format)
                read_offset += bytes_per_pixel
                texture_data[i * 4 : (i + 1) * 4] = decode_function(self, pixel_int)  # noqa
        elif bits_per_pixel == 24:
            bytes_per_pixel = 3
            for i in range(len(image_data) // bytes_per_pixel):
                image_pixel: bytes = image_handler.get_bytes(read_offset, bytes_per_pixel)
                pixel_int: int = image_entry_read_function(image_pixel, image_endianess_format)
                read_offset += bytes_per_pixel
                texture_data[i * 4: (i + 1) * 4] = decode_function(self, pixel_int)  # noqa
        elif bits_per_pixel == 32:
            bytes_per_pixel = 4
            for i in range(len(image_data) // bytes_per_pixel):
                image_pixel: bytes = image_handler.get_bytes(read_offset, bytes_per_pixel)
                pixel_int: int = image_entry_read_function(image_pixel, image_endianess_format)
                read_offset += bytes_per_pixel
                texture_data[i * 4: (i + 1) * 4] = decode_function(self, pixel_int)  # noqa
        elif bits_per_pixel == 48:
            bytes_per_pixel = 6
            for i in range(len(image_data) // bytes_per_pixel):
                image_pixel: bytes = image_handler.get_bytes(read_offset, bytes_per_pixel)
                pixel_int: int = image_entry_read_function(image_pixel, image_endianess_format)
                read_offset += bytes_per_pixel
                texture_data[i * 4: (i + 1) * 4] = decode_function(self, pixel_int)  # noqa
        else:
            raise Exception(f"Bpp {bits_per_pixel} not supported!")

        return texture_data

    def _decode_indexed(self, image_data: bytes, palette_data: bytes, img_width: int,
                        img_height: int, image_format: ImageFormats, image_endianess: str, palette_endianess: str) -> bytes:
        decode_function, bits_per_pixel, palette_entry_size, palette_entry_read_function = self.indexed_data_formats[image_format]
        image_handler = BytesHandler(image_data)
        palette_handler = BytesHandler(palette_data)
        texture_data = bytearray(img_width * img_height * 4)
        image_offset: int = 0
        palette_offset: int = 0
        image_endianess_format: str = self._get_endianess_format(image_endianess)
        palette_endianess_format: str = self._get_endianess_format(palette_endianess)

        palette_data_ints = []
        for i in range(len(palette_data) // palette_entry_size):
            palette_entry = palette_handler.get_bytes(palette_offset, palette_entry_size)
            palette_entry_int = palette_entry_read_function(palette_entry, palette_endianess_format)
            palette_offset += palette_entry_size
            palette_data_ints.append(palette_entry_int)

        if bits_per_pixel == 16:
            for i in range(img_width * img_height):
                if "pal_i8a8" in image_format.value.lower():
                    palette_index: bytes = image_handler.get_bytes(image_offset, 1)
                    alpha_value: bytes = image_handler.get_bytes(image_offset+1, 1)
                    palette_index_int: int = struct.unpack(image_endianess_format + "B", palette_index)[0]
                    alpha_value_int: int = struct.unpack(image_endianess_format + "B", alpha_value)[0]
                    output_bytes: bytes = decode_function(self, palette_data_ints[palette_index_int])  # noqa

                    decoded_bytes: bytearray = bytearray(4)
                    if alpha_value_int < 255:
                        decoded_bytes[0] = output_bytes[0] * alpha_value_int // 255
                        decoded_bytes[1] = output_bytes[1] * alpha_value_int // 255
                        decoded_bytes[2] = output_bytes[2] * alpha_value_int // 255
                        decoded_bytes[3] = alpha_value_int
                    else:
                        decoded_bytes[0] = output_bytes[0]
                        decoded_bytes[1] = output_bytes[1]
                        decoded_bytes[2] = output_bytes[2]
                        decoded_bytes[3] = alpha_value_int

                    texture_data[i * 4:(i + 1) * 4] = decoded_bytes
                else:
                    palette_index = image_handler.get_bytes(image_offset, 2)
                    palette_index_int = struct.unpack(image_endianess_format + "H", palette_index)[0]
                    texture_data[i * 4:(i + 1) * 4] = decode_function(self, palette_data_ints[palette_index_int])  # noqa
                image_offset += 2
        elif bits_per_pixel == 8:
            for i in range(img_width * img_height):
                palette_index = image_handler.get_bytes(image_offset, 1)
                palette_index_int = struct.unpack(image_endianess_format + "B", palette_index)[0]
                texture_data[i * 4:(i + 1) * 4] = decode_function(self, palette_data_ints[palette_index_int])  # noqa
                image_offset += 1
        elif bits_per_pixel == 4:
            for i in range(0, img_width * img_height, 2):
                palette_index = image_handler.get_bytes(image_offset, 1)
                palette_index_int = struct.unpack(image_endianess_format + "B", palette_index)[0]
                if image_endianess == "little":
                    texture_data[i * 4:(i + 1) * 4] = decode_function(self, palette_data_ints[palette_index_int & 0xf])  # noqa
                    texture_data[(i + 1) * 4:(i + 2) * 4] = decode_function(self, palette_data_ints[(palette_index_int >> 4) & 0xf])  # noqa
                elif image_endianess == "big":
                    texture_data[i * 4:(i + 1) * 4] = decode_function(self, palette_data_ints[(palette_index_int >> 4) & 0xf])  # noqa
                    texture_data[(i + 1) * 4:(i + 2) * 4] =decode_function(self, palette_data_ints[palette_index_int & 0xf])  # noqa
                else:
                    raise Exception(f"Endianess not supported! Endianess: {image_endianess}")
                image_offset += 1

        return texture_data

    def decode_image(self, image_data: bytes, img_width: int, img_height: int, image_format: ImageFormats, image_endianess: str = "little") -> bytes:
        return self._decode_generic(image_data, img_width, img_height, self.generic_data_formats[image_format], image_endianess)

    def decode_indexed_image(self, image_data: bytes, palette_data: bytes, img_width: int, img_height: int, image_format: ImageFormats, image_endianess: str = "little", palette_endianess: str = "little") -> bytes:
        return self._decode_indexed(image_data, palette_data, img_width, img_height, image_format, image_endianess, palette_endianess)

    def decode_compressed_image(self, image_data: bytes, img_width: int, img_height: int, image_format: ImageFormats) -> bytes:
        compressed_decoder = CompressedImageDecoder()
        return compressed_decoder.decode_compressed_image_main(image_data, img_width, img_height, image_format)

    def decode_gst_image(self, image_data: bytes, palette_data: bytes, img_width: int, img_height: int, image_format: ImageFormats, convert_format: ImageFormats, is_swizzled: bool = True) -> bytes:
        gst_decoder = GSTImageDecoder()
        decoded_gst_data: bytes = gst_decoder.decode_gst_image_main(image_data, img_width, img_height, image_format, is_swizzled)
        return self.decode_indexed_image(decoded_gst_data, palette_data, img_width, img_height, convert_format)

    def decode_yuv_image(self, image_data: bytes, img_width: int, img_height: int, image_format: ImageFormats) -> bytes:
        yuv_decoder = YUVDecoder()
        return yuv_decoder.decode_yuv_image_main(image_data, img_width, img_height, image_format)

    def decode_bumpmap_image(self, image_data: bytes, img_width: int, img_height: int, image_format: ImageFormats) -> bytes:
        bumpmap_decoder = BumpmapDecoder()
        return bumpmap_decoder.decode_bumpmap_image_main(image_data, img_width, img_height, image_format)

    def decode_n64_image(self, image_data: bytes, img_width: int, img_height: int, image_format: ImageFormats) -> bytes:
        n64_decoder = N64Decoder()
        return n64_decoder.decode_n64_image_main(image_data, img_width, img_height, image_format)
