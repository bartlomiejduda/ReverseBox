"""
Copyright © 2025  Bartłomiej Duda
License: GPL-3.0 License
"""

import ctypes
from ctypes import POINTER, c_int, c_uint8, cast, create_string_buffer

from reversebox.common.common import get_dll_path
from reversebox.common.logger import get_logger
from reversebox.image.image_formats import ImageFormats

logger = get_logger(__name__)

# fmt: off
# mypy: ignore-errors


pvrtexlib_format_mapping: dict[ImageFormats, int] = {
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
    }


class PvrTexlibImageDecoderEncoder:
    """
    Decoder/Encoder for any compressed images like ASTC, ETC1 etc.
    """

    def __init__(self):
        pass

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
        c_image_width = c_int(img_width)
        c_image_height = c_int(img_height)

        input_buffer = create_string_buffer(bytes(image_data))
        c_input_buffer = cast(input_buffer, POINTER(c_uint8))  # buffer with input image data
        c_output_buffer = (c_uint8 * output_buffer_size)()  # empty buffer for output image data

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
