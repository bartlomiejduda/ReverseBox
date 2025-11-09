"""
Copyright © 2025  Bartłomiej Duda
License: GPL-3.0 License
"""

from reversebox.common.logger import get_logger
from reversebox.image.common import get_bpp_for_image_format
from reversebox.image.image_formats import ImageFormats

logger = get_logger(__name__)

# fmt: off


class PSPDXTDecoder:

    def __init__(self):
        pass

    def _get_pitch_align(self, image_format: ImageFormats) -> int:
        if image_format in (ImageFormats.PSP_DXT1, ImageFormats.PSP_DXT3, ImageFormats.PSP_DXT5):
            return 4
        raise Exception(f"Format not supported: {image_format}")

    def _get_pitch(self, bpp: int, img_width: int, image_format: ImageFormats) -> int:
        pitch: int = (bpp * img_width + 7) // 8
        align: int = self._get_pitch_align(image_format)
        return (pitch + align - 1) // align * align

    def _interpolation_50_50(self, c0: int, c1: int) -> int:
        b0, g0, r0, a0 = (c0 >> 24) & 0xFF, (c0 >> 16) & 0xFF, (c0 >> 8) & 0xFF, c0 & 0xFF
        b1, g1, r1, a1 = (c1 >> 24) & 0xFF, (c1 >> 16) & 0xFF, (c1 >> 8) & 0xFF, c1 & 0xFF
        return (((b0 + b1) // 2) << 24) | (((g0 + g1) // 2) << 16) | (((r0 + r1) // 2) << 8) | ((a0 + a1) // 2)

    def _interpolation_66_33(self, c0: int, c1: int) -> int:
        b0, g0, r0, a0 = (c0 >> 24) & 0xFF, (c0 >> 16) & 0xFF, (c0 >> 8) & 0xFF, c0 & 0xFF
        b1, g1, r1, a1 = (c1 >> 24) & 0xFF, (c1 >> 16) & 0xFF, (c1 >> 8) & 0xFF, c1 & 0xFF
        return (((2 * b0 + b1) // 3) << 24) | (((2 * g0 + g1) // 3) << 16) | (((2 * r0 + r1) // 3) << 8) | ((2 * a0 + a1) // 3)

    def _rgb565_to_bgra8888(self, pixel_int: int) -> int:
        r = ((pixel_int >> 11) & 0x1F) * 0xFF // 0x1F
        g = ((pixel_int >> 5) & 0x3F) * 0xFF // 0x3F
        b = ((pixel_int >> 0) & 0x1F) * 0xFF // 0x1F
        a = 0xFF
        return (b << 24) | (g << 16) | (r << 8) | a

    def _decode_psp_dxt1_block(self, image_data: bytes) -> bytearray:
        # Read two 16-bit colors (little endian)
        sp: list[int] = [int.from_bytes(image_data[0:2], 'little'),
                         int.from_bytes(image_data[2:4], 'little'),
                         int.from_bytes(image_data[4:6], 'little'),
                         int.from_bytes(image_data[6:8], 'little')]

        c0: int = sp[2]
        c1: int = sp[3]
        colors: list[int] = [0, 0, 0, 0]
        decoded_dxt_block: bytearray = bytearray(16 * 4)  # 16 RGBA pixels

        if c0 > c1:
            colors[0] = c0 = self._rgb565_to_bgra8888(c0)
            colors[1] = c1 = self._rgb565_to_bgra8888(c1)
            colors[2] = self._interpolation_66_33(c0, c1)
            colors[3] = self._interpolation_66_33(c1, c0)
        else:
            colors[0] = c0 = self._rgb565_to_bgra8888(c0)
            colors[1] = c1 = self._rgb565_to_bgra8888(c1)
            colors[2] = self._interpolation_50_50(c0, c1)
            colors[3] = 0x00  # transparent

        cp = image_data[:4]
        dst_index = 0
        for i in range(4):
            bits = cp[i]
            for _ in range(4):
                color = colors[bits & 0x03]
                decoded_dxt_block[dst_index:dst_index + 4] = [
                    (color >> 8) & 0xFF,  # R
                    (color >> 16) & 0xFF,  # G
                    (color >> 24) & 0xFF,  # B
                    color & 0xFF  # A
                ]
                dst_index += 4
                bits >>= 2

        return decoded_dxt_block

    def _decode_psp_dxt3_block(self, decoded_dxt_block: bytearray, image_data: bytes) -> bytearray:
        sp_offset = 4 * 2
        sp = image_data[sp_offset:]
        dp_index = 3

        for i in range(4):
            bits = int.from_bytes(sp[i * 2:i * 2 + 2], 'little')
            for j in range(4):
                decoded_dxt_block[dp_index] = (bits & 0xF) * 0x11
                dp_index += 4
                bits >>= 4

        return decoded_dxt_block

    def _decode_psp_dxt5_block(self, decoded_dxt_block: bytearray, image_data: bytes) -> bytearray:
        sp_offset = 4 * 2
        sp = image_data[sp_offset:]

        alphas = [0] * 8
        a0 = sp[6]
        a1 = sp[7]
        alphas[0] = a0
        alphas[1] = a1

        if a0 > a1:
            alphas[2] = (a0 * 6 + a1 * 1 + 3) // 7
            alphas[3] = (a0 * 5 + a1 * 2 + 3) // 7
            alphas[4] = (a0 * 4 + a1 * 3 + 3) // 7
            alphas[5] = (a0 * 3 + a1 * 4 + 3) // 7
            alphas[6] = (a0 * 2 + a1 * 5 + 3) // 7
            alphas[7] = (a0 * 1 + a1 * 6 + 3) // 7
        else:
            alphas[2] = (a0 * 4 + a1 * 1 + 2) // 5
            alphas[3] = (a0 * 3 + a1 * 2 + 2) // 5
            alphas[4] = (a0 * 2 + a1 * 3 + 2) // 5
            alphas[5] = (a0 * 1 + a1 * 4 + 2) // 5
            alphas[6] = 0
            alphas[7] = 255

        dp_index = 3

        for i in range(4):
            bits = int.from_bytes(sp[i:i + 4], 'little') >> (i * 4)
            for j in range(4):
                decoded_dxt_block[dp_index] = alphas[bits & 0x7]
                dp_index += 4
                bits >>= 3

        return decoded_dxt_block

    def decode_psp_dxt_image_main(self, image_data: bytes, img_width: int, img_height: int, image_format: ImageFormats) -> bytes:

        bpp: int = get_bpp_for_image_format(image_format)
        pitch: int = self._get_pitch(bpp, img_width, image_format)
        decoded_data: bytearray = bytearray(img_width * img_height * 4)

        for y in range(0, img_height, 4):
            for x in range(0, img_width, 4):
                src_offset = pitch * y + (bpp * x // 8) * 4
                src_block = image_data[src_offset:src_offset + 16]  # DXT block

                if image_format == ImageFormats.PSP_DXT1:
                    decoded_block = self._decode_psp_dxt1_block(src_block)
                elif image_format == ImageFormats.PSP_DXT3:
                    decoded_block = self._decode_psp_dxt3_block(self._decode_psp_dxt1_block(src_block), src_block)
                elif image_format == ImageFormats.PSP_DXT5:
                    decoded_block = self._decode_psp_dxt5_block(self._decode_psp_dxt1_block(src_block), src_block)
                    pass
                else:
                    raise Exception(f"Image format not supported by PSP DXT decoder! Image_format: {image_format}")

                # Copy decoded block to output buffer
                for i in range(16):
                    dx = x + (i % 4)
                    dy = y + (i // 4)
                    if dx >= img_width or dy >= img_height:
                        continue
                    pix_index = (img_width * dy + dx) * 4
                    decoded_data[pix_index:pix_index + 4] = decoded_block[i * 4:i * 4 + 4]

        return bytes(decoded_data)
