"""
Copyright © 2024  Bartłomiej Duda
License: GPL-3.0 License
"""
import struct

from PIL import Image

from reversebox.common.common import calculate_padding_length
from reversebox.common.logger import get_logger
from reversebox.image.compression.compression_gst import decompress_gst_image
from reversebox.image.image_formats import ImageFormats
from reversebox.image.swizzling.swizzle_gst import (
    unswizzle_detail1,
    unswizzle_detail2,
    unswizzle_gst_base,
)
from reversebox.io_files.bytes_handler import BytesHandler
from reversebox.io_files.bytes_helper_functions import (
    get_uint8,
    get_uint16,
    get_uint24,
    get_uint32,
)

logger = get_logger(__name__)

# fmt: off
# mypy: ignore-errors


class ImageDecoder:
    def __init__(self):
        pass

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

    def _decode_xrgb1555_pixel(self, pixel_int: int) -> bytes:
        p = bytearray(4)
        r = pixel_int & 0x1F
        g = (pixel_int >> 5) & 0x1F
        b = (pixel_int >> 10) & 0x1F
        p[2] = (r << 3) | (r >> 2)
        p[1] = (g << 3) | (g >> 2)
        p[0] = (b << 3) | (b >> 2)
        p[3] = 0xFF
        return p

    def _decode_abgr1555_pixel(self, pixel_int: int) -> bytes:
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

    def _decode_xbgr1555_pixel(self, pixel_int: int) -> bytes:
        p = bytearray(4)
        r = pixel_int & 0x1F
        g = (pixel_int >> 5) & 0x1F
        b = (pixel_int >> 10) & 0x1F
        p[0] = (r << 3) | (r >> 2)
        p[1] = (g << 3) | (g >> 2)
        p[2] = (b << 3) | (b >> 2)
        p[3] = 0xFF
        return p

    def _decode_rgb565_pixel(self, pixel_int: int) -> bytes:
        p = bytearray(4)
        p[0] = ((pixel_int >> 11) & 0x1F) * 0xFF // 0x1F
        p[1] = ((pixel_int >> 5) & 0x3F) * 0xFF // 0x3F
        p[2] = ((pixel_int >> 0) & 0x1F) * 0xFF // 0x1F
        p[3] = 0xFF
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

    def _decode_bgra8888_pixel(self, pixel_int: int) -> bytes:
        p = bytearray(4)
        p[2] = (pixel_int >> 0) & 0xff
        p[1] = (pixel_int >> 8) & 0xff
        p[0] = (pixel_int >> 16) & 0xff
        p[3] = (pixel_int >> 24) & 0xff
        return p

    def _decode_argb8888_pixel(self, pixel_int: int) -> bytes:
        p = bytearray(4)
        p[2] = (pixel_int >> 0) & 0xff
        p[1] = (pixel_int >> 8) & 0xff
        p[0] = (pixel_int >> 16) & 0xff
        p[3] = (pixel_int >> 24) & 0xff
        return p

    def _decode_argb4444_pixel(self, pixel_int: int) -> bytes:
        p = bytearray(4)
        a = (pixel_int >> 12) & 0xff
        r = (pixel_int >> 8) & 0x0f
        g = (pixel_int >> 4) & 0x0f
        b = (pixel_int >> 0) & 0x0f

        p[0] = (r << 4) | (r >> 0)
        p[1] = (g << 4) | (g >> 0)
        p[2] = (b << 4) | (b >> 0)
        p[3] = (a << 4) | (a >> 0)
        return p

    def _decode_rgba4444_pixel(self, pixel_int: int) -> bytes:
        p = bytearray(4)
        a = (pixel_int >> 12) & 0xff
        r = (pixel_int >> 8) & 0x0f
        g = (pixel_int >> 4) & 0x0f
        b = (pixel_int >> 0) & 0x0f

        p[0] = (b << 4) | (b >> 0)
        p[1] = (g << 4) | (g >> 0)
        p[2] = (r << 4) | (r >> 0)
        p[3] = (a << 4) | (a >> 0)
        return p

    def _decode_yuy2_pixel(self, Y: float, U: float, V: float) -> bytes:
        p = bytearray(4)

        def _round_clamp_int(f: float) -> int:
            i: int = int(f+0.5)
            if i < 0:
                i = 0
            if i > 255:
                i = 255
            return i

        C: float = Y - 16.0
        D: float = U - 128.0
        E: float = V - 128.0

        R: float = 1.164383 * C + 1.596027 * E
        G: float = 1.164383 * C - (0.391762 * D) - (0.812968 * E)
        B: float = 1.164383 * C + 2.017232 * D

        p[0] = _round_clamp_int(R)
        p[1] = _round_clamp_int(G)
        p[2] = _round_clamp_int(B)
        p[3] = 0xFF
        return p

    generic_data_formats = {
        # image_format: (decode_function, bits_per_pixel, image_entry_read_function)
        ImageFormats.RGBX2222: (_decode_rgbx2222_pixel, 8, get_uint8),
        ImageFormats.RGBA2222: (_decode_rgba2222_pixel, 8, get_uint8),
        ImageFormats.RGB565: (_decode_rgb565_pixel, 16, get_uint16),
        ImageFormats.RGB888: (_decode_rgb888_pixel, 24, get_uint24),
        ImageFormats.BGR888: (_decode_bgr888_pixel, 24, get_uint24),
        ImageFormats.ARGB4444: (_decode_argb4444_pixel, 16, get_uint16),
        ImageFormats.RGBA4444: (_decode_rgba4444_pixel, 16, get_uint16),
        ImageFormats.XRGB1555: (_decode_xrgb1555_pixel, 16, get_uint16),
        ImageFormats.ABGR1555: (_decode_abgr1555_pixel, 16, get_uint16),
        ImageFormats.XBGR1555: (_decode_xbgr1555_pixel, 16, get_uint16),
        ImageFormats.ARGB8888: (_decode_argb8888_pixel, 32, get_uint32),
    }

    indexed_data_formats = {
        # image_format: (decode_function, bits_per_pixel, palette_entry_size, palette_entry_read_function)
        ImageFormats.PAL4_RGBX5551: (_decode_rgbx5551_pixel, 4, 2, get_uint16),
        ImageFormats.PAL4_RGB888: (_decode_rgb888_pixel, 4, 3, get_uint24),
        ImageFormats.PAL4_RGBA8888: (_decode_rgba8888_pixel, 4, 4, get_uint32),
        ImageFormats.PAL8_RGBX2222: (_decode_rgbx2222_pixel, 8, 1, get_uint8),
        ImageFormats.PAL8_RGBX5551: (_decode_rgbx5551_pixel, 8, 2, get_uint16),
        ImageFormats.PAL8_RGB888: (_decode_rgb888_pixel, 8, 3, get_uint24),
        ImageFormats.PAL8_RGBA8888: (_decode_rgba8888_pixel, 8, 4, get_uint32),
        ImageFormats.PAL8_BGRA8888: (_decode_bgra8888_pixel, 8, 4, get_uint32),
    }

    compressed_data_formats = {
        # image format: (decoder_name, decoder_arg)
        ImageFormats.DXT1: ("bcn", 1),
        ImageFormats.DXT3: ("bcn", 2),
        ImageFormats.DXT5: ("bcn", 3)
    }

    gst_data_formats = {
        # image_format: (block_width, block_height, detail_bpp)
        ImageFormats.GST121: (1, 2, 1),
        ImageFormats.GST221: (2, 2, 1),
        ImageFormats.GST421: (4, 2, 1),
        ImageFormats.GST821: (8, 2, 1),
        ImageFormats.GST122: (1, 2, 2),
        ImageFormats.GST222: (2, 2, 2),
        ImageFormats.GST422: (4, 2, 2),
        ImageFormats.GST822: (8, 2, 2),
    }

    yuv_data_formats = {
        # image_format: (decode_function, bpp)
        ImageFormats.YUY2: (_decode_yuy2_pixel, 32),
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

        if bits_per_pixel == 8:
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
        else:
            raise Exception(f"Bpp {bits_per_pixel} not supported!")

        return texture_data

    def _decode_indexed(self, image_data: bytes, palette_data: bytes, img_width: int,
                        img_height: int, image_format: tuple, image_endianess: str, palette_endianess: str) -> bytes:
        decode_function, bits_per_pixel, palette_entry_size, palette_entry_read_function = image_format
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
                texture_data[i * 4:(i + 1) * 4] = decode_function(self, palette_data_ints[palette_index_int & 0xf])  # noqa
                texture_data[(i + 1) * 4:(i + 2) * 4] = decode_function(self, palette_data_ints[(palette_index_int >> 4) & 0xf])  # noqa
                image_offset += 1

        return texture_data

    def _decode_compressed(self, image_data: bytes, img_width: int, img_height: int, image_format: tuple) -> bytes:
        decoder_name, decoder_arg = image_format
        pil_img = Image.frombuffer(
            "RGBA",
            (img_width, img_height),
            image_data,
            decoder_name,
            decoder_arg,
            "",
        )
        return pil_img.tobytes()

    def _decode_gst(self, image_data: bytes, palette_data: bytes, img_width: int, img_height: int, image_format: tuple, convert_format: ImageFormats, is_swizzled: bool) -> bytes:
        block_width, block_height, detail_bpp = image_format

        size_of_base: int = (img_width // block_width) * (img_height // block_height)
        detail_offset: int = size_of_base + calculate_padding_length(size_of_base, 16)

        base_data: bytes = image_data[:size_of_base]
        detail_data: bytes = image_data[detail_offset:]

        # unswizzle GST data
        if is_swizzled:
            base_data = unswizzle_gst_base(base_data, img_width, img_height, block_width, block_height)
            if detail_bpp == 2:
                detail_data = unswizzle_detail2(detail_data, img_width, img_height)
            else:
                detail_data = unswizzle_detail1(detail_data, img_width, img_height)

        # decompress GST data
        decompressed_texture_data: bytes = decompress_gst_image(base_data, detail_data, img_width, img_height, block_width, block_height, detail_bpp)

        # convert indexed image to RGBA to get final result
        output_texture_data = self.decode_indexed_image(
            decompressed_texture_data,
            palette_data,
            img_width,
            img_height,
            convert_format
        )

        return output_texture_data

    def _decode_yuv(self, image_data: bytes, img_width: int, img_height: int, image_format: tuple):
        decode_function, bpp = image_format
        is_odd: bool = True if (img_width & 1) else False
        current_yuv_offset: int = 0
        current_pixel_number: int = 0
        output_texture_data = bytearray(img_width * img_height * 4)

        for y in range(img_height):
            for x in range(0, img_width, 2):

                Y0: float = float(image_data[current_yuv_offset])
                U: float = float(image_data[current_yuv_offset + 1])
                Y1: float = float(image_data[current_yuv_offset + 2])
                V: float = float(image_data[current_yuv_offset + 3])

                pixel1 = decode_function(self, Y0, U, V)
                pixel2 = decode_function(self, Y1, U, V)
                output_texture_data[current_pixel_number * 4:(current_pixel_number + 1) * 4] = pixel1
                output_texture_data[(current_pixel_number + 1) * 4:(current_pixel_number + 2) * 4] = pixel2

                if is_odd and x == img_width - 1:
                    current_yuv_offset += 4
                    current_pixel_number += 1
                else:
                    current_yuv_offset += 4
                    current_pixel_number += 2

        return output_texture_data

    def decode_image(self, image_data: bytes, img_width: int, img_height: int, image_format: ImageFormats, image_endianess: str = "little") -> bytes:
        return self._decode_generic(image_data, img_width, img_height, self.generic_data_formats[image_format], image_endianess)

    def decode_indexed_image(self, image_data: bytes, palette_data: bytes, img_width: int, img_height: int, image_format: ImageFormats, image_endianess: str = "little", palette_endianess: str = "little") -> bytes:
        return self._decode_indexed(image_data, palette_data, img_width, img_height, self.indexed_data_formats[image_format], image_endianess, palette_endianess)

    def decode_compressed_image(self, image_data: bytes, img_width: int, img_height: int, image_format: ImageFormats) -> bytes:
        return self._decode_compressed(image_data, img_width, img_height, self.compressed_data_formats[image_format])

    def decode_gst_image(self, image_data: bytes, palette_data: bytes, img_width: int, img_height: int, image_format: ImageFormats, convert_format: ImageFormats, is_swizzled: bool = True) -> bytes:
        return self._decode_gst(image_data, palette_data, img_width, img_height, self.gst_data_formats[image_format], convert_format, is_swizzled)

    def decode_yuv_image(self, image_data: bytes, img_width: int, img_height: int, image_format: ImageFormats):
        return self._decode_yuv(image_data, img_width, img_height, self.yuv_data_formats[image_format])
