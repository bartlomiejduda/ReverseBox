"""
Copyright © 2024-2025  Bartłomiej Duda
License: GPL-3.0 License
"""

import ctypes
import faulthandler
import os
import tempfile
from ctypes import (
    POINTER,
    Structure,
    c_int,
    c_long,
    c_size_t,
    c_uint8,
    cast,
    create_string_buffer,
)

from reversebox.common.common import get_dll_path
from reversebox.common.constants import DLL_LOG_FILE_NAME
from reversebox.common.logger import get_logger
from reversebox.image.common import get_bc_image_data_size
from reversebox.image.image_formats import ImageFormats

logger = get_logger(__name__)

# fmt: off
# mypy: ignore-errors


class DXGIImage(Structure):
    """
    Structure needed for DirectXTex library
    """
    _fields_ = [
        ("width", c_size_t),
        ("height", c_size_t),
        ("format", c_int),
        ("rowPitch", c_size_t),
        ("slicePitch", c_size_t),
        ("pixels", POINTER(c_uint8))
    ]


class CompressedImageDecoderEncoder:
    """
    Decoder/Encoder for any compressed images like BC1/DXT1, BC2/DXT2 etc.
    """

    def __init__(self):
        with open(os.path.join(tempfile.gettempdir(), DLL_LOG_FILE_NAME), "a", encoding="utf-8") as f:
            faulthandler.enable(f)

    def _init_dxgi_image(self, img_width: int, img_height: int, format_number: int,
                         row_pitch: int, slice_pitch: int, image_data: bytes) -> DXGIImage:
        image = DXGIImage()
        image.width = img_width
        image.height = img_height
        image.format = format_number
        image.rowPitch = row_pitch
        image.slicePitch = slice_pitch

        if image_data and len(image_data) > 0:
            buffer = create_string_buffer(bytes(image_data))
            image.pixels = cast(buffer, POINTER(c_uint8))  # buffer with input image data
        else:
            data_size = img_width * img_height * 4
            image.pixels = (c_uint8 * data_size)()  # empty buffer for output image data

        return image

    def _get_dxgi_format_number(self, image_format: ImageFormats) -> int:
        """
        Mapping ReverseBox formats to DXGI formats
        https://learn.microsoft.com/en-us/windows/win32/api/dxgiformat/ne-dxgiformat-dxgi_format
        """

        if image_format == ImageFormats.BC1_DXT1:
            return 71
        elif image_format == ImageFormats.BC2_DXT3:
            return 74
        elif image_format == ImageFormats.BC3_DXT5:
            return 77
        elif image_format == ImageFormats.BC4_UNORM:
            return 80
        elif image_format == ImageFormats.BC5_UNORM:
            return 83
        elif image_format == ImageFormats.BC6H_UF16:
            return 95
        elif image_format == ImageFormats.BC6H_SF16:
            return 96
        elif image_format == ImageFormats.BC7_UNORM:
            return 98
        elif image_format == ImageFormats.RGBA8888:
            return 28
        else:
            raise Exception(f"Not supported image format! Image_format: {image_format}")

    def _convert_directxtex_image(self, image_data: bytes, img_width: int, img_height: int, image_format: ImageFormats, encode_flag: bool) -> bytes:
        """
        Function used for decoding/encoding compressed BC formats
        """
        dll_path: str = get_dll_path("DirectXTex.dll")
        if encode_flag:
            input_format_number: int = self._get_dxgi_format_number(ImageFormats.RGBA8888)
            output_format_number: int = self._get_dxgi_format_number(image_format)
        else:
            input_format_number: int = self._get_dxgi_format_number(image_format)
            output_format_number: int = self._get_dxgi_format_number(ImageFormats.RGBA8888)

        # calculating pitch params
        c_input_format_number = c_int(input_format_number)
        c_output_format_number = c_int(output_format_number)
        c_image_width = c_int(img_width)
        c_image_height = c_int(img_height)
        c_input_row_pitch = c_long(0)
        c_output_row_pitch = c_long(0)
        c_input_slice_pitch = c_long(0)
        c_output_slice_pitch = c_long(0)
        c_flags = c_int(0)

        # encode params
        c_threshold = ctypes.c_float(0.5)
        c_nullptr = (c_uint8 * 100)()

        try:
            dll_file = ctypes.CDLL(dll_path)
            dll_file.ComputePitch(c_input_format_number, c_image_width, c_image_height, ctypes.byref(c_input_row_pitch), ctypes.byref(c_input_slice_pitch), c_flags)
            dll_file.ComputePitch(c_output_format_number, c_image_width, c_image_height, ctypes.byref(c_output_row_pitch), ctypes.byref(c_output_slice_pitch), c_flags)

        except Exception as error:
            raise Exception(f"Error while calculating pitch! Error: {error}")

        # initializing structure logic
        input_dxgi_image: DXGIImage = self._init_dxgi_image(img_width, img_height, input_format_number, c_input_row_pitch.value, c_input_slice_pitch.value, image_data)
        output_dxgi_image: DXGIImage = self._init_dxgi_image(img_width, img_height, output_format_number, c_output_row_pitch.value, c_output_slice_pitch.value, b'')

        # decompressing/compressing image logic
        try:
            dll_file = ctypes.CDLL(dll_path)

            if encode_flag:
                h_result = dll_file.CompressBC(ctypes.byref(input_dxgi_image), ctypes.byref(output_dxgi_image),
                                               c_flags, c_flags,
                                               c_threshold, c_nullptr)
            else:
                h_result = dll_file.DecompressBC(ctypes.byref(input_dxgi_image), ctypes.byref(output_dxgi_image))
        except Exception as error:
            raise Exception(f"Error while decoding compressed data! Error: {error}")

        if h_result != 0:
            raise Exception(f"DLL decompression failed! H_result: {h_result}")

        if encode_flag:
            converted_data_size: int = get_bc_image_data_size(img_height, img_width, image_format)
        else:
            converted_data_size: int = img_height * img_width * 4
        converted_data = bytearray((c_uint8 * converted_data_size).from_address(ctypes.addressof(output_dxgi_image.pixels.contents)))
        return converted_data

    def decode_compressed_image_main(self, image_data: bytes, img_width: int, img_height: int, image_format: ImageFormats) -> bytes:
        return self._convert_directxtex_image(image_data, img_width, img_height, image_format, False)

    def encode_compressed_image_main(self, image_data: bytes, img_width: int, img_height: int, image_format: ImageFormats) -> bytes:
        return self._convert_directxtex_image(image_data, img_width, img_height, image_format, True)
