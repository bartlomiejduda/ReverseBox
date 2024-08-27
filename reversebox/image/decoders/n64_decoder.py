"""
Copyright © 2024  Bartłomiej Duda
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


class N64Decoder:

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

        output_data = crop_image(output_data, _width, _height, 32, img_width, img_height)
        return output_data

    def decode_n64_image_main(self, image_data: bytes, img_width: int, img_height: int, image_format: ImageFormats) -> bytes:

        if image_format == ImageFormats.N64_RGBA32:
            return self._decode_n64_rgba32_image(image_data, img_width, img_height, 4, 4)
        elif image_format == ImageFormats.N64_CMPR:
            return self._decode_n64_cmpr_image(image_data, img_width, img_height, 8, 8)
        else:
            raise Exception(f"Image format not supported by N64 decoder! Image_format: {image_format}")
