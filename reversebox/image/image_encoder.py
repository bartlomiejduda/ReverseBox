"""
Copyright © 2024-2025  Bartłomiej Duda
License: GPL-3.0 License
"""

from typing import Dict, List, Tuple

from PIL import Image

from reversebox.common.logger import get_logger
from reversebox.image.common import (
    convert_bpp_to_bytes_per_pixel,
    get_bpp_for_image_format,
)
from reversebox.image.decoders.compressed_decoder_encoder import (
    CompressedImageDecoderEncoder,
)
from reversebox.image.image_formats import ImageFormats
from reversebox.image.pillow_wrapper import PillowWrapper
from reversebox.io_files.bytes_handler import BytesHandler
from reversebox.io_files.bytes_helper_functions import (
    get_uint16,
    get_uint24,
    get_uint32,
    set_uint8,
    set_uint16,
    set_uint24,
    set_uint32,
)

logger = get_logger(__name__)

# fmt: off
# mypy: ignore-errors


class ImageEncoder:

    pillow_wrapper = PillowWrapper()

    def __init__(self):
        pass

    def _encode_rgba8888_pixel(self, pixel_int: int) -> bytes:
        p = bytearray(4)
        p[0] = (pixel_int >> 0) & 0xff
        p[1] = (pixel_int >> 8) & 0xff
        p[2] = (pixel_int >> 16) & 0xff
        p[3] = (pixel_int >> 24) & 0xff
        return p

    def _encode_bgra8888_pixel(self, pixel_int: int) -> bytes:
        p = bytearray(4)
        p[0] = (pixel_int >> 16) & 0xff
        p[1] = (pixel_int >> 8) & 0xff
        p[2] = (pixel_int >> 0) & 0xff
        p[3] = (pixel_int >> 24) & 0xff
        return p

    def _encode_argb8888_pixel(self, pixel_int: int) -> bytes:
        p = bytearray(4)
        p[0] = (pixel_int >> 24) & 0xff
        p[1] = (pixel_int >> 0) & 0xff
        p[2] = (pixel_int >> 8) & 0xff
        p[3] = (pixel_int >> 16) & 0xff
        return p

    def _encode_bgr565_pixel(self, pixel_int: int) -> bytearray:
        r = (pixel_int >> 0) & 0xFF
        g = (pixel_int >> 8) & 0xFF
        b = (pixel_int >> 16) & 0xFF

        r5 = (r >> 3) & 0x1F
        g6 = (g >> 2) & 0x3F
        b5 = (b >> 3) & 0x1F

        rgb565 = (r5 << 11) | (g6 << 5) | b5

        rgb565_bytes = bytearray(2)
        rgb565_bytes[0] = rgb565 & 0xFF
        rgb565_bytes[1] = (rgb565 >> 8) & 0xFF
        return rgb565_bytes

    def _encode_rgb565_pixel(self, pixel_int: int) -> bytearray:
        b = (pixel_int >> 0) & 0xFF
        g = (pixel_int >> 8) & 0xFF
        r = (pixel_int >> 16) & 0xFF

        b5 = (b >> 3) & 0x1F
        g6 = (g >> 2) & 0x3F
        r5 = (r >> 3) & 0x1F

        bgr565 = (r5 << 11) | (g6 << 5) | b5

        bgr565_bytes = bytearray(2)
        bgr565_bytes[0] = bgr565 & 0xFF
        bgr565_bytes[1] = (bgr565 >> 8) & 0xFF
        return bgr565_bytes

    def _encode_rgb888_pixel(self, pixel_int: int) -> bytearray:
        p = bytearray(3)
        p[0] = (pixel_int >> 0) & 0xff
        p[1] = (pixel_int >> 8) & 0xff
        p[2] = (pixel_int >> 16) & 0xff
        return p

    def _encode_bgr888_pixel(self, pixel_int: int) -> bytearray:
        p = bytearray(3)
        p[0] = (pixel_int >> 16) & 0xff
        p[1] = (pixel_int >> 8) & 0xff
        p[2] = (pixel_int >> 0) & 0xff
        return p

    def _encode_abgr4444_pixel(self, pixel_int: int) -> bytearray:
        p = bytearray(2)

        b = pixel_int & 0xFF
        a = (pixel_int >> 8) & 0xFF
        r = (pixel_int >> 16) & 0xFF
        g = (pixel_int >> 24) & 0xFF

        r4 = (r >> 4) & 0x0F
        g4 = (g >> 4) & 0x0F
        b4 = (b >> 4) & 0x0F
        a4 = (a >> 4) & 0x0F

        rgba4444 = (r4 << 12) | (g4 << 8) | (b4 << 4) | a4

        p[0] = (rgba4444 >> 8) & 0xFF
        p[1] = rgba4444 & 0xFF
        return p

    def _encode_bgra4444_pixel(self, pixel_int: int) -> bytearray:
        p = bytearray(2)

        r = pixel_int & 0xFF
        g = (pixel_int >> 8) & 0xFF
        b = (pixel_int >> 16) & 0xFF
        a = (pixel_int >> 24) & 0xFF

        r4 = (r >> 4) & 0x0F
        g4 = (g >> 4) & 0x0F
        b4 = (b >> 4) & 0x0F
        a4 = (a >> 4) & 0x0F

        bgra4444 = (a4 << 12) | (r4 << 8) | (g4 << 4) | b4

        p[0] = bgra4444 & 0xFF
        p[1] = (bgra4444 >> 8) & 0xFF
        return p

    def _encode_rgbx4444_pixel(self, pixel_int: int) -> bytearray:
        p = bytearray(2)

        r = pixel_int & 0xFF
        g = (pixel_int >> 8) & 0xFF
        b = (pixel_int >> 16) & 0xFF
        x = 0xFF

        r4 = (r >> 4) & 0x0F
        g4 = (g >> 4) & 0x0F
        b4 = (b >> 4) & 0x0F
        x4 = (x >> 4) & 0x0F

        rgbx4444 = (x4 << 12) | (b4 << 8) | (g4 << 4) | r4

        p[0] = rgbx4444 & 0xFF
        p[1] = (rgbx4444 >> 8) & 0xFF
        return p

    def _encode_rgba5551_pixel(self, pixel_int: int) -> bytearray:
        p = bytearray(2)

        r = pixel_int & 0xFF
        g = (pixel_int >> 8) & 0xFF
        b = (pixel_int >> 16) & 0xFF
        a = (pixel_int >> 24) & 0xFF

        r5 = r >> 3
        g5 = g >> 3
        b5 = b >> 3
        a1 = 1 if a >= 128 else 0

        rgba5551 = (a1 << 15) | (b5 << 10) | (g5 << 5) | r5

        p[0] = rgba5551 & 0xFF
        p[1] = (rgba5551 >> 8) & 0xFF
        return p

    def _encode_bgra5551_pixel(self, pixel_int: int) -> bytearray:
        p = bytearray(2)

        r = pixel_int & 0xFF
        g = (pixel_int >> 8) & 0xFF
        b = (pixel_int >> 16) & 0xFF
        a = (pixel_int >> 24) & 0xFF

        r5 = r >> 3
        g5 = g >> 3
        b5 = b >> 3
        a1 = 1 if a >= 128 else 0

        rgba5551 = (a1 << 15) | (r5 << 10) | (g5 << 5) | b5

        p[0] = rgba5551 & 0xFF
        p[1] = (rgba5551 >> 8) & 0xFF
        return p

    def _encode_rgbx5551_pixel(self, pixel_int: int) -> bytearray:
        p = bytearray(2)

        r = pixel_int & 0xFF
        g = (pixel_int >> 8) & 0xFF
        b = (pixel_int >> 16) & 0xFF

        r5 = r >> 3
        g5 = g >> 3
        b5 = b >> 3
        a1 = 0xFF

        rgbx5551 = (a1 << 15) | (b5 << 10) | (g5 << 5) | r5

        p[0] = rgbx5551 & 0xFF
        p[1] = (rgbx5551 >> 8) & 0xFF
        return p

    def _encode_rgbt5551_pixel(self, pixel_int: int) -> bytearray:
        p = bytearray(2)

        r = pixel_int & 0xFF
        g = (pixel_int >> 8) & 0xFF
        b = (pixel_int >> 16) & 0xFF
        a = (pixel_int >> 24) & 0xFF

        r5 = r >> 3
        g5 = g >> 3
        b5 = b >> 3

        rgbt5551 = (b5 << 10) | (g5 << 5) | r5

        if a < 25*255//100:  # transparent
            rgbt5551 = 0
        elif a >= 75*255//100:  # opaque
            if not rgbt5551:
                rgbt5551 = (1 << 10)
        else:  # translucient
            rgbt5551 |= 0x8000

        p[0] = rgbt5551 & 0xFF
        p[1] = (rgbt5551 >> 8) & 0xFF
        return p

    # source format is always RGBA8888
    # target format is one of the listed below
    generic_data_formats = {
        # image_format: (encode_function, bits_per_pixel, read_function, write_function)
        ImageFormats.RGB565: (_encode_rgb565_pixel, 16, get_uint16, set_uint16),
        ImageFormats.BGR565: (_encode_bgr565_pixel, 16, get_uint16, set_uint16),
        ImageFormats.ABGR4444: (_encode_abgr4444_pixel, 16, get_uint16, set_uint16),
        ImageFormats.BGRA4444: (_encode_bgra4444_pixel, 16, get_uint16, set_uint16),
        ImageFormats.RGBX4444: (_encode_rgbx4444_pixel, 16, get_uint16, set_uint16),
        ImageFormats.RGBA5551: (_encode_rgba5551_pixel, 16, get_uint16, set_uint16),
        ImageFormats.BGRA5551: (_encode_bgra5551_pixel, 16, get_uint16, set_uint16),
        ImageFormats.RGBX5551: (_encode_rgbx5551_pixel, 16, get_uint16, set_uint16),
        ImageFormats.RGBT5551: (_encode_rgbt5551_pixel, 16, get_uint16, set_uint16),
        ImageFormats.RGB888: (_encode_rgb888_pixel, 24, get_uint24, set_uint24),
        ImageFormats.BGR888: (_encode_bgr888_pixel, 24, get_uint24, set_uint24),
        ImageFormats.RGBA8888: (_encode_rgba8888_pixel, 32, get_uint32, set_uint32),
        ImageFormats.BGRA8888: (_encode_bgra8888_pixel, 32, get_uint32, set_uint24),
        ImageFormats.ARGB8888: (_encode_argb8888_pixel, 32, get_uint32, set_uint24),
    }

    def _get_endianess_format(self, endianess: str) -> str:
        if endianess == "little":
            endianess_format = "<"
        elif endianess == "big":
            endianess_format = ">"
        else:
            raise Exception("Wrong endianess!")
        return endianess_format

    def _encode_generic(self, image_data: bytes, img_width: int, img_height: int, image_format: ImageFormats, image_endianess: str) -> bytes:
        encode_function, bits_per_pixel, _, _ = self.generic_data_formats[image_format]
        image_handler = BytesHandler(image_data)
        source_image_bytes_per_pixel = 4  # always 4 for RGBA8888

        if bits_per_pixel == 4:
            texture_data = bytearray(img_width * img_height // 2)
        elif bits_per_pixel == 8:
            texture_data = bytearray(img_width * img_height)
        elif bits_per_pixel == 16:
            texture_data = bytearray(img_width * img_height * 2)
        elif bits_per_pixel == 24:
            texture_data = bytearray(img_width * img_height * 3)
        elif bits_per_pixel == 32:
            texture_data = bytearray(img_width * img_height * 4)
        else:
            raise Exception(f"[1] Bits_per_pixel={bits_per_pixel} not supported!")

        read_offset = 0
        image_endianess_format: str = self._get_endianess_format(image_endianess)

        for i in range(len(image_data) // source_image_bytes_per_pixel):
            image_pixel: bytes = image_handler.get_bytes(read_offset, source_image_bytes_per_pixel)
            pixel_int: int = get_uint32(image_pixel, image_endianess_format)
            read_offset += source_image_bytes_per_pixel

            if bits_per_pixel == 4:
                pass
            elif bits_per_pixel == 8:
                pass
            elif bits_per_pixel == 16:
                texture_data[i * 2: (i + 1) * 2] = encode_function(self, pixel_int)  # noqa
            elif bits_per_pixel == 24:
                texture_data[i * 3: (i + 1) * 3] = encode_function(self, pixel_int)  # noqa
            elif bits_per_pixel == 32:
                texture_data[i * 4: (i + 1) * 4] = encode_function(self, pixel_int)  # noqa
            else:
                raise Exception(f"[2] Bits_per_pixel={bits_per_pixel} not supported!")

        return texture_data

    def _encode_indexed(self, image_data: bytes, img_width: int,
                        img_height: int, image_format: ImageFormats, palette_format: ImageFormats, image_endianess: str, palette_endianess: str, max_colors_count: int) -> Tuple[bytes, bytes]:
        encode_function, palette_bpp, read_function, write_function = self.generic_data_formats[palette_format]
        image_bpp: int = get_bpp_for_image_format(image_format)
        palette_bpp: int = get_bpp_for_image_format(palette_format)
        palette_bytes_per_pixel: int = convert_bpp_to_bytes_per_pixel(palette_bpp)
        image_bytes_per_pixel: int = convert_bpp_to_bytes_per_pixel(image_bpp)
        image_endianess_format: str = self._get_endianess_format(image_endianess)

        # prepare empty bytearray for output data
        if image_bpp == 4:
            texture_data = bytearray(img_width * img_height // 2)
        elif image_bpp == 8:
            texture_data = bytearray(img_width * img_height)
        elif image_bpp == 16:
            texture_data = bytearray(img_width * img_height * 2)
        elif image_bpp == 24:
            texture_data = bytearray(img_width * img_height * 3)
        elif image_bpp == 32:
            texture_data = bytearray(img_width * img_height * 4)
        else:
            raise Exception(f"[1] Image_bits_per_pixel={image_bpp} not supported!")

        texture_data_expected_size: int = len(texture_data)

        # colour quantization and dithering
        pillow_img: Image = PillowWrapper().get_pillow_image_from_rgba8888_data(image_data, img_width, img_height)
        unique_colors_count: int = len(set(pillow_img.getdata()))
        if unique_colors_count > max_colors_count:
            pillow_img = pillow_img.quantize(colors=max_colors_count, method=2).convert("RGBA", dither=Image.Dither.FLOYDSTEINBERG)
        image_data = pillow_img.tobytes()

        # encode to intermediate image (e.g. RGBA8888 -> RGB565)
        encoded_intermediate_image: bytes = self._encode_generic(image_data, img_width, img_height, palette_format, image_endianess)

        # get pixels from intermediate image
        pixel_int_values: list[int] = []
        if image_bpp in (4, 8):
            number_of_pixels: int = len(encoded_intermediate_image) // palette_bytes_per_pixel
            for i in range(number_of_pixels):
                pixel_bytes: bytes = encoded_intermediate_image[i * palette_bytes_per_pixel: (i + 1) * palette_bytes_per_pixel]
                pixel_int: int = read_function(pixel_bytes, image_endianess_format)
                pixel_int_values.append(pixel_int)
        else:
            raise Exception(f"Not supported img_bpp={image_bpp}!")  # TODO - support other formats like PAL16

        # get aligned number of colors
        if max_colors_count <= 4:  # PAL2 (4-color)
            aligned_colors_count = 4
        elif max_colors_count <= 16:  # PAL4 (16-color)
            aligned_colors_count = 16
        elif max_colors_count <= 256:  # PAL8 (256-color)
            aligned_colors_count = 256
        else:
            raise Exception(f"Not supported aligned colors count for max_colors_count={max_colors_count}")  # TODO - support other formats like PAL16

        palette_data: bytearray = bytearray(aligned_colors_count * palette_bytes_per_pixel)
        palette_data_expected_size: int = len(palette_data)

        # palette preparation (get unique values for palette)
        pixel_check_list: List[int] = []
        pixel_map: Dict[int, int] = {}
        pal_entry_number: int = 0
        for pixel_value in pixel_int_values:
            if pixel_value not in pixel_check_list:
                pixel_map[pixel_value] = pal_entry_number
                pal_entry_number += 1
            pixel_check_list.append(pixel_value)

        # encode palette
        pal_entry_number = 0
        for map_entry_key, map_entry_value in pixel_map.items():
            pal_entry_bytes: bytes = write_function(map_entry_key, image_endianess_format)
            palette_data[pal_entry_number * palette_bytes_per_pixel: (pal_entry_number + 1) * palette_bytes_per_pixel] = pal_entry_bytes
            pal_entry_number += 1

        # encode indices
        img_entry_number: int = 0
        if image_bpp == 4:  # PAL4
            for i in range(0, len(pixel_int_values), 2):
                pal_entry_number_1: int = pixel_map[pixel_int_values[i]]
                pal_entry_number_2: int = pixel_map[pixel_int_values[i+1]]
                if palette_endianess == "little":
                    pal_entry_combined: int = ((pal_entry_number_2 << 4) | pal_entry_number_1) & 0xFF
                else:
                    pal_entry_combined: int = ((pal_entry_number_1 << 4) | pal_entry_number_2) & 0xFF
                pixel_bytes: bytes = set_uint8(pal_entry_combined, image_endianess_format)
                texture_data[img_entry_number * image_bytes_per_pixel: (img_entry_number + 1) * image_bytes_per_pixel] = pixel_bytes
                img_entry_number += 1

        elif image_bpp == 8:  # PAL8
            for pixel_int_value in pixel_int_values:
                pal_entry_number: int = pixel_map[pixel_int_value]
                pixel_bytes: bytes = set_uint8(pal_entry_number, image_endianess_format)
                texture_data[img_entry_number * image_bytes_per_pixel: (img_entry_number + 1) * image_bytes_per_pixel] = pixel_bytes
                img_entry_number += 1

        else:
            raise Exception(f"Not supported img_bpp={image_bpp}!")  # TODO - support other formats like PAL16

        # final checks
        if len(palette_data) > palette_data_expected_size or len(palette_data) > 1024:
            raise Exception("Error! Palette data too big!")

        if len(texture_data) > texture_data_expected_size:
            raise Exception("Error! Texture data too big!")

        return texture_data, palette_data

    def encode_image(self, image_data: bytes, img_width: int, img_height: int, image_format: ImageFormats, image_endianess: str = "little") -> bytes:
        return self._encode_generic(image_data, img_width, img_height, image_format, image_endianess)

    def encode_indexed_image(self, image_data: bytes, img_width: int, img_height: int, image_format: ImageFormats, palette_format: ImageFormats, max_color_count: int, image_endianess: str = "little", palette_endianess: str = "little") -> Tuple[bytes, bytes]:
        return self._encode_indexed(image_data, img_width, img_height, image_format, palette_format, image_endianess, palette_endianess, max_color_count)

    def encode_compressed_image(self, image_data: bytes, img_width: int, img_height: int, image_format: ImageFormats) -> bytes:
        return CompressedImageDecoderEncoder().encode_compressed_image_main(image_data, img_width, img_height, image_format)
