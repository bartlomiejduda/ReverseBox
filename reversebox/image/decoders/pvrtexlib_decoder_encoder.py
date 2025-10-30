"""
Copyright © 2025  Bartłomiej Duda
License: GPL-3.0 License
"""

import ctypes
import faulthandler
import os
import tempfile
from ctypes import POINTER, c_int, c_uint, c_uint8, c_void_p, cast, create_string_buffer

from reversebox.common.common import get_dll_path
from reversebox.common.constants import DLL_LOG_FILE_NAME
from reversebox.common.logger import get_logger
from reversebox.image.image_formats import ImageFormats

logger = get_logger(__name__)

# fmt: off
# mypy: ignore-errors


pvrtexlib_format_mapping: dict[ImageFormats, int] = {
        ImageFormats.PVRTCI_2bpp_RGB: 10,
        ImageFormats.PVRTCI_2bpp_RGBA: 11,
        ImageFormats.PVRTCI_4bpp_RGB: 12,
        ImageFormats.PVRTCI_4bpp_RGBA: 13,
        ImageFormats.PVRTCII_2bpp: 14,
        ImageFormats.PVRTCII_4bpp: 15,
        ImageFormats.ETC1: 16,

        ImageFormats.BC1_DXT1: 20,
        ImageFormats.DXT2: 21,
        ImageFormats.BC2_DXT3: 22,
        ImageFormats.DXT4: 23,
        ImageFormats.BC3_DXT5: 24,

        ImageFormats.BC4_UNORM: 33,
        ImageFormats.BC5_UNORM: 34,

        ImageFormats.YUV422_UYVY: 40,
        ImageFormats.YUV422_YUY2: 41,

        ImageFormats.BW1bpp: 50,
        ImageFormats.SharedExponentR9G9B9E5: 51,
        ImageFormats.RGBG8888: 52,
        ImageFormats.GRGB8888: 53,
        ImageFormats.ETC2_RGB: 54,
        ImageFormats.ETC2_RGBA: 55,
        ImageFormats.ETC2_RGB_A1: 56,
        ImageFormats.EAC_R11: 57,
        ImageFormats.EAC_RG11: 58,

        ImageFormats.ASTC_4x4: 60,
        ImageFormats.ASTC_5x4: 61,
        ImageFormats.ASTC_5x5: 62,
        ImageFormats.ASTC_6x5: 63,
        ImageFormats.ASTC_6x6: 64,
        ImageFormats.ASTC_8x5: 65,
        ImageFormats.ASTC_8x6: 66,
        ImageFormats.ASTC_8x8: 67,
        ImageFormats.ASTC_10x5: 68,
        ImageFormats.ASTC_10x6: 69,
        ImageFormats.ASTC_10x8: 70,
        ImageFormats.ASTC_10x10: 71,
        ImageFormats.ASTC_12x10: 72,
        ImageFormats.ASTC_12x12: 73,

        ImageFormats.ASTC_3x3x3: 80,
        ImageFormats.ASTC_4x3x3: 81,
        ImageFormats.ASTC_4x4x3: 82,
        ImageFormats.ASTC_4x4x4: 83,
        ImageFormats.ASTC_5x4x4: 84,
        ImageFormats.ASTC_5x5x4: 85,
        ImageFormats.ASTC_5x5x5: 86,
        ImageFormats.ASTC_6x5x5: 87,
        ImageFormats.ASTC_6x6x5: 88,
        ImageFormats.ASTC_6x6x6: 89,

        ImageFormats.BASISU_ETC1S: 100,
        ImageFormats.BASISU_UASTC: 101,

        ImageFormats.RGBM: 102,
        ImageFormats.RGBD: 103
    }


class PvrTexlibImageDecoderEncoder:
    """
    Decoder/Encoder for any compressed images like ASTC, ETC1 etc.
    """

    def __init__(self):
        with open(os.path.join(tempfile.gettempdir(), DLL_LOG_FILE_NAME), "a", encoding="utf-8") as f:
            faulthandler.enable(f)

    def _get_pvrtexlib_format_number(self, image_format: ImageFormats) -> int:
        """
        Mapping ReverseBox formats to PvrTexLib formats
        """

        try:
            return pvrtexlib_format_mapping[image_format]
        except KeyError:
            raise Exception(f"Not supported image format! Image_format: {image_format}")

    def _convert_pvrtexlib_image(self, image_data: bytes, img_width: int, img_height: int, image_format: ImageFormats, encode_flag: bool) -> bytes:
        """
        Function used for decoding/encoding compressed PvrTexlib formats
        """
        dll_path: str = get_dll_path("PVRTexLibWrapper.dll")

        input_format_number: int = self._get_pvrtexlib_format_number(image_format)
        output_buffer_size: int = img_height * img_width * 4

        c_format_number = c_int(input_format_number)
        c_image_width = c_uint(img_width)
        c_image_height = c_uint(img_height)

        input_buffer = create_string_buffer(bytes(image_data))
        c_input_buffer = cast(input_buffer, POINTER(c_void_p))  # buffer with input image data
        c_output_buffer = (c_void_p * output_buffer_size)()  # empty buffer for output image data

        try:
            dll_file = ctypes.CDLL(dll_path)

            if encode_flag:
                output_size: int = dll_file.EncodeByPVRTexLib(
                    c_input_buffer,
                    c_output_buffer,
                    c_format_number,
                    c_image_width,
                    c_image_height
                )
            else:
                output_size: int = dll_file.DecodeByPVRTexLib(
                    c_input_buffer,
                    c_output_buffer,
                    c_format_number,
                    c_image_width,
                    c_image_height
                )
        except Exception as error:
            raise Exception(f"Error! Error: {error}")

        if output_size == 0:
            raise Exception("Output texture is empty!")

        converted_data = bytearray((c_uint8 * output_size).from_address(ctypes.addressof(c_output_buffer)))
        return converted_data

    def decode_compressed_image_main(self, image_data: bytes, img_width: int, img_height: int, image_format: ImageFormats) -> bytes:
        return self._convert_pvrtexlib_image(image_data, img_width, img_height, image_format, False)

    def encode_compressed_image_main(self, image_data: bytes, img_width: int, img_height: int, image_format: ImageFormats) -> bytes:
        return self._convert_pvrtexlib_image(image_data, img_width, img_height, image_format, True)
