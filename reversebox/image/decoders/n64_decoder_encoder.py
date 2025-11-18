"""
Copyright © 2024-2025  Bartłomiej Duda
License: GPL-3.0 License
"""

from reversebox.common.logger import get_logger
from reversebox.image.common import crop_image, get_storage_wh
from reversebox.image.image_formats import ImageFormats
from reversebox.io_files.bytes_handler import BytesHandler
from reversebox.io_files.bytes_helper_functions import get_uint8, get_uint16

logger = get_logger(__name__)

# fmt: off
# mypy: ignore-errors


class N64ImageDecoderEncoder:

    def __init__(self):
        pass

    def _decode_n64_rgba32_image(self, image_data: bytes, img_width: int, img_height: int, block_width: int, block_height: int) -> bytes:
        _width, _height = get_storage_wh(img_width, img_height, block_width, block_height)
        output_data = bytearray(_width * _height * 4)
        offset = 0

        for y in range(0, _height, block_height):
            for x in range(0, _width, block_width):
                for y2 in range(block_height):
                    for x2 in range(block_width):
                        idx = (((y + y2) * _width) + (x + x2)) * 4
                        output_data[idx + 0] = image_data[offset + 1]
                        output_data[idx + 1] = image_data[offset + 32]
                        output_data[idx + 2] = image_data[offset + 33]
                        output_data[idx + 3] = image_data[offset + 0]
                        offset += 2
                offset += 32

        output_data = crop_image(output_data, _width, _height, 32, img_width, img_height)
        return output_data

    def _decode_n64_cmpr_image(self, image_data: bytes, img_width: int, img_height: int, block_width: int, block_height: int) -> bytes:
        _width, _height = get_storage_wh(img_width, img_height, block_width, block_height)
        output_data = bytearray(_width * _height * 4)
        image_data_handler = BytesHandler(image_data)

        def _decode_rgb565_pixel(pixel_int: int) -> bytes:
            p = bytearray(4)
            p[0] = ((pixel_int >> 11) & 0x1F) * 0xFF // 0x1F
            p[1] = ((pixel_int >> 5) & 0x3F) * 0xFF // 0x3F
            p[2] = ((pixel_int >> 0) & 0x1F) * 0xFF // 0x1F
            p[3] = 0xFF
            return p

        current_offset: int = 0
        for y in range(0, _height, block_height):
            for x in range(0, _width, block_width):
                for y2 in range(0, block_height, 4):
                    for x2 in range(0, block_width, 4):

                        c0 = get_uint16(image_data_handler.get_bytes(current_offset, 2), ">")
                        current_offset += 2
                        c1 = get_uint16(image_data_handler.get_bytes(current_offset, 2), ">")
                        current_offset += 2

                        c = [
                            _decode_rgb565_pixel(c0),
                            _decode_rgb565_pixel(c1),
                            bytearray(4),
                            bytearray(4)
                        ]

                        if c0 > c1:
                            for i in range(4):
                                c[2][i] = int((2 * c[0][i] + c[1][i]) / 3)
                                c[3][i] = int((2 * c[1][i] + c[0][i]) / 3)
                        else:
                            for i in range(4):
                                c[2][i] = int((c[0][i] + c[1][i]) * .5)
                                c[3][i] = 0

                        for y3 in range(4):
                            b = get_uint8(image_data_handler.get_bytes(current_offset, 1), ">")
                            current_offset += 1
                            for x3 in range(4):
                                idx = (((y + y2 + y3) * _width) + (x + x2 + x3)) * 4
                                output_data[idx: idx + 4] = c[(b >> (6 - (x3 * 2))) & 0x3]

        return output_data

    def _encode_n64_cmpr_image(self, rgba_data: bytes, img_width: int, img_height: int,
                               block_width: int, block_height: int) -> bytes:

        def encode_rgb565(r: int, g: int, b: int) -> int:
            r5 = (r * 31) // 255
            g6 = (g * 63) // 255
            b5 = (b * 31) // 255
            return (r5 << 11) | (g6 << 5) | b5

        def decode565_to_rgba(c: int) -> tuple:
            return (
                ((c >> 11) & 0x1F) * 255 // 0x1F,
                ((c >> 5) & 0x3F) * 255 // 0x3F,
                (c & 0x1F) * 255 // 0x1F,
                255
            )

        def get_pixel(x: int, y: int, w: int) -> tuple:
            idx = (y * w + x) * 4
            return rgba_data[idx], rgba_data[idx + 1], rgba_data[idx + 2], rgba_data[idx + 3]

        _width, _height = get_storage_wh(img_width, img_height, block_width, block_height)
        out = bytearray()

        for y in range(0, _height, block_height):
            for x in range(0, _width, block_width):
                for y2 in range(0, block_height, 4):
                    for x2 in range(0, block_width, 4):

                        block: list = []
                        for dy in range(4):
                            for dx in range(4):
                                px = x + x2 + dx
                                py = y + y2 + dy
                                if px < img_width and py < img_height:
                                    block.append(get_pixel(px, py, img_width))
                                else:
                                    block.append((0, 0, 0, 0))

                        opaque_pixels = [p for p in block if p[3] >= 128]
                        alpha_mode = len(opaque_pixels) != len(block)

                        if len(opaque_pixels) == 0:
                            c0 = 0
                            c1 = 0
                            p0 = decode565_to_rgba(c0)
                            p1 = decode565_to_rgba(c1)
                        else:
                            r_min = min(p[0] for p in opaque_pixels)
                            g_min = min(p[1] for p in opaque_pixels)
                            b_min = min(p[2] for p in opaque_pixels)

                            r_max = max(p[0] for p in opaque_pixels)
                            g_max = max(p[1] for p in opaque_pixels)
                            b_max = max(p[2] for p in opaque_pixels)

                            c0 = encode_rgb565(r_max, g_max, b_max)
                            c1 = encode_rgb565(r_min, g_min, b_min)

                            if alpha_mode and (c0 > c1):
                                c0, c1 = c1, c0

                            p0 = decode565_to_rgba(c0)
                            p1 = decode565_to_rgba(c1)

                        if c0 > c1:
                            p2 = (
                                (2 * p0[0] + p1[0]) // 3,
                                (2 * p0[1] + p1[1]) // 3,
                                (2 * p0[2] + p1[2]) // 3,
                                255
                            )
                            p3 = (
                                (2 * p1[0] + p0[0]) // 3,
                                (2 * p1[1] + p0[1]) // 3,
                                (2 * p1[2] + p0[2]) // 3,
                                255
                            )
                        else:
                            p2 = (
                                (p0[0] + p1[0]) // 2,
                                (p0[1] + p1[1]) // 2,
                                (p0[2] + p1[2]) // 2,
                                255
                            )
                            p3 = (0, 0, 0, 0)

                        palette = [p0, p1, p2, p3]
                        out += bytes([(c0 >> 8) & 0xFF, c0 & 0xFF])
                        out += bytes([(c1 >> 8) & 0xFF, c1 & 0xFF])

                        for row in range(4):
                            i0 = row * 4 + 0
                            i1 = row * 4 + 1
                            i2 = row * 4 + 2
                            i3 = row * 4 + 3

                            def best_index_for_pixel(px):
                                r, g, b, a = px
                                if alpha_mode and a < 128:
                                    return 3
                                best = 0
                                best_d = 10 ** 12
                                max_index = 3 if (not (alpha_mode and palette[3][3] == 0)) else 2
                                for pi in range(0, max_index + 1):
                                    pr, pg, pb, pa = palette[pi]
                                    d = (r - pr) ** 2 + (g - pg) ** 2 + (b - pb) ** 2
                                    if d < best_d:
                                        best_d = d
                                        best = pi
                                return best

                            idx0 = best_index_for_pixel(block[i0])
                            idx1 = best_index_for_pixel(block[i1])
                            idx2 = best_index_for_pixel(block[i2])
                            idx3 = best_index_for_pixel(block[i3])

                            b = (idx0 << 6) | (idx1 << 4) | (idx2 << 2) | (idx3 << 0)
                            out.append(b)

        return bytes(out)

    def decode_n64_image_main(self, image_data: bytes, img_width: int, img_height: int, image_format: ImageFormats) -> bytes:

        if image_format == ImageFormats.N64_RGBA32:
            return self._decode_n64_rgba32_image(image_data, img_width, img_height, 4, 4)
        elif image_format == ImageFormats.N64_CMPR:
            return self._decode_n64_cmpr_image(image_data, img_width, img_height, 8, 8)
        else:
            raise Exception(f"Image format not supported by N64 decoder! Image_format: {image_format}")

    def encode_n64_image_main(self, image_data: bytes, img_width: int, img_height: int, image_format: ImageFormats) -> bytes:

        if image_format == ImageFormats.N64_CMPR:
            return self._encode_n64_cmpr_image(image_data, img_width, img_height, 8, 8)
        else:
            raise Exception(f"Image format not supported by N64 decoder! Image_format: {image_format}")
