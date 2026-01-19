"""
Copyright © 2024-2026  Bartłomiej Duda
License: GPL-3.0 License
"""

from typing import List, Optional, Tuple

import libimagequant as liq
import numpy as np
import PIL.Image
from PIL import Image

from reversebox.common.logger import get_logger
from reversebox.image.common import (
    convert_bpp_to_bytes_per_pixel,
    get_bpp_for_image_format,
)
from reversebox.image.decoders.compressed_decoder_encoder import (
    CompressedImageDecoderEncoder,
)
from reversebox.image.decoders.gst_decoder_encoder import GSTImageDecoderEncoder
from reversebox.image.decoders.n64_decoder_encoder import N64ImageDecoderEncoder
from reversebox.image.decoders.pvrtexlib_decoder_encoder import (
    PvrTexlibImageDecoderEncoder,
)
from reversebox.image.image_formats import ImageFormats
from reversebox.image.pillow_wrapper import PillowWrapper
from reversebox.io_files.bytes_handler import BytesHandler
from reversebox.io_files.bytes_helper_functions import (
    get_uint8,
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

    def _encode_i4_pixel(self, pixel_int: int) -> bytes:
        r = pixel_int & 0xFF
        value4 = r // 0x11
        return bytes([value4 & 0x0F])

    def _encode_ia4_pixel(self, pixel_int: int) -> bytes:
        r = (pixel_int >> 0) & 0xFF
        a = (pixel_int >> 24) & 0xFF

        intensity4 = ((r + 8) // 17) & 0x0F
        alpha4 = ((a + 8) // 17) & 0x0F

        ia4 = (alpha4 << 4) | intensity4
        return bytes([ia4])

    def _encode_i8_pixel(self, pixel_int: int) -> bytes:
        r = pixel_int & 0xFF
        return bytes([r])

    def _encode_ia8_pixel(self, pixel_int: int) -> bytes:
        r = (pixel_int >> 0) & 0xFF
        a = (pixel_int >> 24) & 0xFF
        return bytes((r & 0xFF, a & 0xFF))

    def _encode_alpha_17x_pixel(self, pixel_int: int) -> bytes:
        alpha_value = (pixel_int >> 24) & 0xff
        alpha_value = alpha_value // 17
        return bytes([alpha_value])

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

    def _encode_bgr5a3_pixel(self, pixel_int: int) -> bytearray:
        r = (pixel_int >> 0) & 0xFF
        g = (pixel_int >> 8) & 0xFF
        b = (pixel_int >> 16) & 0xFF
        a = (pixel_int >> 24) & 0xFF

        if a >= 248:
            r5 = (r * 31 + 127) // 255
            g5 = (g * 31 + 127) // 255
            b5 = (b * 31 + 127) // 255
            pixel = (0x8000 | (r5 << 10) | (g5 << 5) | (b5 << 0))
        else:
            r4 = (r * 15 + 127) // 255
            g4 = (g * 15 + 127) // 255
            b4 = (b * 15 + 127) // 255
            a3 = (a * 7 + 127) // 255
            pixel = ((a3 << 12) | (r4 << 8) | (g4 << 4) | (b4 << 0))

        return bytearray([pixel & 0xFF, (pixel >> 8) & 0xFF])

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
        ImageFormats.GRAY4: (_encode_i4_pixel, 4, get_uint8, set_uint8),
        ImageFormats.ALPHA4_17X: (_encode_alpha_17x_pixel, 4, get_uint8, set_uint8),
        ImageFormats.N64_IA4: (_encode_ia4_pixel, 8, get_uint8, set_uint8),
        ImageFormats.GRAY8: (_encode_i8_pixel, 8, get_uint8, set_uint8),
        ImageFormats.N64_IA8: (_encode_ia8_pixel, 16, get_uint8, set_uint8),
        ImageFormats.RGB565: (_encode_rgb565_pixel, 16, get_uint16, set_uint16),
        ImageFormats.BGR565: (_encode_bgr565_pixel, 16, get_uint16, set_uint16),
        ImageFormats.N64_BGR5A3: (_encode_bgr5a3_pixel, 16, get_uint16, set_uint16),
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
        ImageFormats.BGRA8888: (_encode_bgra8888_pixel, 32, get_uint32, set_uint32),
        ImageFormats.ARGB8888: (_encode_argb8888_pixel, 32, get_uint32, set_uint32),
    }

    def _get_endianess_format(self, endianess: str) -> str:
        if endianess == "little":
            endianess_format = "<"
        elif endianess == "big":
            endianess_format = ">"
        else:
            raise Exception("Wrong endianess!")
        return endianess_format

    def _encode_generic_image(self, image_data: bytes, img_width: int, img_height: int, image_format: ImageFormats, image_endianess: str) -> bytes:
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
        source_image_endianess_format: str = self._get_endianess_format("little")  # always RGBA8888 little endian

        if bits_per_pixel == 4:
            for i in range(img_width * img_height // 2):
                image_pixel: bytes = image_handler.get_bytes(read_offset, source_image_bytes_per_pixel)
                pixel_int: int = get_uint32(image_pixel, source_image_endianess_format)
                read_offset += source_image_bytes_per_pixel
                encoded_pixel_data1 = encode_function(self, pixel_int)

                image_pixel: bytes = image_handler.get_bytes(read_offset, source_image_bytes_per_pixel)
                pixel_int: int = get_uint32(image_pixel, source_image_endianess_format)
                read_offset += source_image_bytes_per_pixel
                encoded_pixel_data2 = encode_function(self, pixel_int)

                if image_endianess == "little":
                    encoded_pixel = (encoded_pixel_data2[0] << 4) | encoded_pixel_data1[0]
                elif image_endianess == "big":
                    encoded_pixel = (encoded_pixel_data1[0] << 4) | encoded_pixel_data2[0]
                else:
                    raise Exception("Not supported endianess!")
                texture_data[i] = encoded_pixel
        else:
            for i in range(len(image_data) // source_image_bytes_per_pixel):
                image_pixel: bytes = image_handler.get_bytes(read_offset, source_image_bytes_per_pixel)
                pixel_int: int = get_uint32(image_pixel, source_image_endianess_format)
                read_offset += source_image_bytes_per_pixel
                encoded_pixel_data = encode_function(self, pixel_int)  # encode target pixel in little endian order

                if image_endianess == "big":
                    encoded_pixel_data = encoded_pixel_data[::-1]  # change pixel endianess to big endian

                if bits_per_pixel == 8:
                    texture_data[i: (i + 1)] = encoded_pixel_data
                elif bits_per_pixel == 16:
                    texture_data[i * 2: (i + 1) * 2] = encoded_pixel_data
                elif bits_per_pixel == 24:
                    texture_data[i * 3: (i + 1) * 3] = encoded_pixel_data
                elif bits_per_pixel == 32:
                    texture_data[i * 4: (i + 1) * 4] = encoded_pixel_data
                else:
                    raise Exception(f"[2] Bits_per_pixel={bits_per_pixel} not supported!")

        return texture_data

    def _encode_generic(self, image_data: bytes, img_width: int, img_height: int, image_format: ImageFormats,
                        image_endianess: str, number_of_mipmaps: int, mipmaps_resampling_type: PIL.Image.Resampling) -> bytes:
        # main image logic
        encoded_texture_data: bytes = self._encode_generic_image(image_data, img_width, img_height, image_format, image_endianess)

        # mipmaps logic
        if number_of_mipmaps > 0:
            base_img: Image = PillowWrapper().get_pillow_image_from_rgba8888_data(
                image_data, img_width, img_height
            )
            mip_width: int = img_width
            mip_height: int = img_height
            for i in range(number_of_mipmaps):
                mip_width //= 2
                mip_height //= 2
                mip_pillow_img: Image = base_img.resize((mip_width, mip_height), resample=mipmaps_resampling_type)
                mip_rgba_data: bytes = PillowWrapper().get_image_data_from_pillow_image(mip_pillow_img)
                encoded_mipmap_data: bytes = self._encode_generic_image(mip_rgba_data, mip_width, mip_height, image_format, image_endianess)
                encoded_texture_data += encoded_mipmap_data

        return encoded_texture_data

    def _encode_indexed_calculate_output_size(self, image_bpp: int, img_width: int, img_height: int) -> int:
        if image_bpp == 4:
            return img_width * img_height // 2
        elif image_bpp == 8:
            return img_width * img_height
        elif image_bpp == 16:
            return img_width * img_height * 2
        elif image_bpp == 24:
            return img_width * img_height * 3
        elif image_bpp == 32:
            return img_width * img_height * 4
        else:
            raise Exception(f"[1] Image_bits_per_pixel={image_bpp} not supported!")

    # set list of indices in texture data (as bytes)
    def _encode_indexed_encode_indices(self, image_bpp: int, indices_list: list[int],
                                       image_endianess_format: str, image_bytes_per_pixel: int, texture_data_size: int) -> bytes:
        texture_data: bytearray = bytearray(texture_data_size)
        img_entry_number: int = 0
        if image_bpp == 4:  # PAL4
            for i in range(0, len(indices_list), 2):
                pal_index_number_1: int = indices_list[i]
                pal_index_number_2: int = indices_list[i+1]
                if image_endianess_format == "<":  # little endian
                    pal_index_combined: int = ((pal_index_number_2 << 4) | pal_index_number_1) & 0xFF
                else:  # big endian
                    pal_index_combined: int = ((pal_index_number_1 << 4) | pal_index_number_2) & 0xFF
                pal_index_bytes: bytes = set_uint8(pal_index_combined, image_endianess_format)
                texture_data[img_entry_number * image_bytes_per_pixel: (img_entry_number + 1) * image_bytes_per_pixel] = pal_index_bytes
                img_entry_number += 1

        elif image_bpp == 8:  # PAL8
            for pal_index in indices_list:
                pal_index_bytes: bytes = set_uint8(pal_index, image_endianess_format)
                texture_data[img_entry_number * image_bytes_per_pixel: (img_entry_number + 1) * image_bytes_per_pixel] = pal_index_bytes
                img_entry_number += 1

        else:
            raise Exception(f"Not supported img_bpp={image_bpp}!")  # TODO - support other formats like PAL16

        assert len(texture_data) == texture_data_size
        return bytes(texture_data)

    # Input for below function must be:
    # image_data --> RGBA8888 image data
    # palette_data (optional) --> existing palette in any format (can be extracted from game etc.)
    # palette_format --> format of palette_data (can be game specific)
    def _encode_indexed(self, image_data: bytes, palette_data: Optional[bytes], img_width: int,
                        img_height: int, image_format: ImageFormats, palette_format: ImageFormats,
                        image_endianess: str, palette_endianess: str, max_colors_count: int,
                        number_of_mipmaps: int) -> Tuple[bytes, bytes]:
        # initial checks
        if image_format not in (ImageFormats.PAL4, ImageFormats.PAL8):
            raise Exception(f"Image format {image_format} not supported!")
        if not max_colors_count or max_colors_count > 256 or max_colors_count == 0:
            raise Exception(f"Max number of colors {max_colors_count} is not allowed!")
        if len(image_data) % 4 != 0:
            raise Exception(f"Wrong RGBA data size: {len(image_data)}")

        # get initial values
        number_of_palette_colors: int = max_colors_count
        image_bpp: int = get_bpp_for_image_format(image_format)
        palette_bpp: int = get_bpp_for_image_format(palette_format)
        palette_bytes_per_pixel: int = convert_bpp_to_bytes_per_pixel(palette_bpp)
        image_endianess_format: str = self._get_endianess_format(image_endianess)
        palette_endianess_format: str = self._get_endianess_format(palette_endianess)
        encode_function, _, read_function, write_function = self.generic_data_formats[palette_format]
        texture_data: bytes = b''
        image_bytes_per_pixel: int = convert_bpp_to_bytes_per_pixel(image_bpp)
        main_texture_data_expected_size: int = self._encode_indexed_calculate_output_size(image_bpp, img_width, img_height)

        # define attributes for libimagequant library
        attr = liq.Attr()
        attr.max_colors = number_of_palette_colors
        attr.speed = 1  # 1 = best quality (slow), 10 = worst quality (fast)
        attr.min_quality = 1
        attr.max_quality = 100

        # create libimagequant image
        liq_image: liq.Image = attr.create_rgba(image_data, img_width, img_height, gamma=0.0)

        # quantize image with libimagequant algorithm
        quantized_img: liq.Result = liq_image.quantize(attr)

        # get image data and palette after quantization
        quantized_pixels: bytes = quantized_img.remap_image(liq_image)  # PAL8 pixels generated by libimagequant
        out_palette: List[liq.Color] = quantized_img.get_palette()  # List of "Color" objects generated by libimagequant

        # convert liq pixels to indices list
        indices_list: List[int] = [value for value in quantized_pixels]

        # convert liq palette to RGBA8888 color list
        unique_palette_values: List[int] = [(color.a << 24) | (color.b << 16) | (color.g << 8) | color.r for color in out_palette]

        # get aligned number of colors
        if max_colors_count <= 4:  # PAL2 (4-color)
            aligned_colors_count = 4
        elif max_colors_count <= 16:  # PAL4 (16-color)
            aligned_colors_count = 16
        elif max_colors_count <= 256:  # PAL8 (256-color)
            aligned_colors_count = 256
        else:
            raise Exception(f"Not supported aligned colors count for max_colors_count={max_colors_count}")  # TODO - support other formats like PAL16

        # encode palette
        if not palette_data:
            # set empty bytearray for palette data
            palette_data: bytearray = bytearray(aligned_colors_count * palette_bytes_per_pixel)

            for pal_entry_number in range(aligned_colors_count):
                if pal_entry_number < len(unique_palette_values):
                    pal_entry_bytes: bytes = encode_function(self, unique_palette_values[pal_entry_number])
                    if image_endianess != "little":
                        pal_entry_bytes = pal_entry_bytes[::-1]  # change endianess to big endian
                else:
                    pal_entry_bytes: bytes = write_function(0, palette_endianess_format)
                assert len(pal_entry_bytes) == palette_bytes_per_pixel
                palette_data[pal_entry_number * palette_bytes_per_pixel: (pal_entry_number + 1) * palette_bytes_per_pixel] = pal_entry_bytes

        # get expected size
        palette_data_expected_size: int = len(palette_data)

        # encode indices for main texture
        main_texture_data: bytes = self._encode_indexed_encode_indices(
            image_bpp,
            indices_list,
            image_endianess_format,
            image_bytes_per_pixel,
            main_texture_data_expected_size
        )
        texture_data += main_texture_data

        # mipmaps logic
        if number_of_mipmaps > 0:
            mipmap_indices = np.array(indices_list, dtype=np.uint8).reshape((img_height, img_width))
            mipmap_image: Image = Image.fromarray(mipmap_indices, mode="L")

            mip_width: int = img_width
            mip_height: int = img_height
            for i in range(number_of_mipmaps):
                mip_width //= 2
                mip_height //= 2

                img_resized: Image = mipmap_image.resize((mip_width, mip_height), Image.Resampling.NEAREST)
                indices_resized: List[int] = np.array(img_resized, dtype=np.uint8).flatten().tolist()

                mipmap_texture_data_expected_size: int = self._encode_indexed_calculate_output_size(image_bpp, mip_width, mip_height)

                # encode indices for mipmap
                mipmap_texture_data: bytes = self._encode_indexed_encode_indices(
                    image_bpp,
                    indices_resized,
                    image_endianess_format,
                    image_bytes_per_pixel,
                    mipmap_texture_data_expected_size
                )

                if len(mipmap_texture_data) != mipmap_texture_data_expected_size:
                    raise Exception("Error! Wrong size of mipmap data!")

                texture_data += mipmap_texture_data
        # end of mipmaps logic

        # final checks
        if len(palette_data) != palette_data_expected_size or len(palette_data) > 1024 or len(palette_data) == 0:
            raise Exception("Error! Wrong size of palette data!")

        if len(main_texture_data) != main_texture_data_expected_size:
            raise Exception("Error! Wrong size of main texture data!")

        return texture_data, palette_data

    def encode_image(self, image_data: bytes, img_width: int, img_height: int, image_format: ImageFormats,
                     image_endianess: str = "little", number_of_mipmaps: int = 0,
                     mipmaps_resampling_type: PIL.Image.Resampling = Image.Resampling.NEAREST) -> bytes:
        return self._encode_generic(image_data, img_width, img_height, image_format, image_endianess, number_of_mipmaps, mipmaps_resampling_type)

    # TODO - add support for "palette data" parameter (not none if palette should be the same for each mipmap)
    def encode_indexed_image(self, image_data: bytes, img_width: int, img_height: int, image_format: ImageFormats,
                             palette_format: ImageFormats, max_color_count: int, image_endianess: str = "little",
                             palette_endianess: str = "little", number_of_mipmaps: int = 0) -> Tuple[bytes, bytes]:
        return self._encode_indexed(image_data, None, img_width, img_height, image_format, palette_format,
                                    image_endianess, palette_endianess, max_color_count, number_of_mipmaps)

    def encode_compressed_image(self, image_data: bytes, img_width: int, img_height: int, image_format: ImageFormats) -> bytes:
        return CompressedImageDecoderEncoder().encode_compressed_image_main(image_data, img_width, img_height, image_format)

    def encode_pvrtexlib_image(self, image_data: bytes, img_width: int, img_height: int, image_format: ImageFormats) -> bytes:
        return PvrTexlibImageDecoderEncoder().encode_compressed_image_main(image_data, img_width, img_height, image_format)

    def encode_n64_image(self, image_data: bytes, img_width: int, img_height: int, image_format: ImageFormats) -> bytes:
        return N64ImageDecoderEncoder().encode_n64_image_main(image_data, img_width, img_height, image_format)

    def encode_gst_image(self, image_data: bytes, img_width: int, img_height: int, gst_format: ImageFormats, image_format: ImageFormats,
                         palette_format: ImageFormats, max_color_count: int, is_swizzled: bool = True) -> bytes:
        encoded_image_data, encoded_palette_data = self.encode_indexed_image(image_data, img_width, img_height, image_format, palette_format, max_color_count)
        return GSTImageDecoderEncoder().encode_gst_image_main(encoded_image_data, encoded_palette_data, img_width, img_height, gst_format, is_swizzled)
