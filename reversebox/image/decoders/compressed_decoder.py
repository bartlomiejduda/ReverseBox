"""
Copyright © 2024  Bartłomiej Duda
License: GPL-3.0 License
"""

import ctypes
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
from reversebox.common.logger import get_logger
from reversebox.image.image_formats import ImageFormats

logger = get_logger(__name__)

# fmt: off


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


class CompressedImageDecoder:
    """
    Decoder for any compressed images like BC1/DXT1, BC2/DXT2 etc.
    """

    def __init__(self):
        pass

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


    def _decode_directxtex_image(self, image_data: bytes, img_width: int, img_height: int, image_format: ImageFormats) -> bytes:
        """
        Function used for decoding compressed BC formats
        """
        dll_path: str = get_dll_path("DirectXTex.dll")
        input_format_number: int = self._get_dxgi_format_number(image_format)
        output_format_number: int = self._get_dxgi_format_number(ImageFormats.RGBA8888)

        # calculating pitch logic
        c_input_format_number = c_int(input_format_number)
        c_output_format_number = c_int(output_format_number)
        c_image_width = c_int(img_width)
        c_image_height = c_int(img_height)
        c_input_row_pitch = c_long(0)
        c_output_row_pitch = c_long(0)
        c_input_slice_pitch = c_long(0)
        c_output_slice_pitch = c_long(0)
        c_flags = c_int(0)

        try:
            dll_file = ctypes.CDLL(dll_path)
            dll_file.ComputePitch(c_input_format_number, c_image_width, c_image_height, ctypes.byref(c_input_row_pitch), ctypes.byref(c_input_slice_pitch), c_flags)
            dll_file.ComputePitch(c_output_format_number, c_image_width, c_image_height, ctypes.byref(c_output_row_pitch), ctypes.byref(c_output_slice_pitch), c_flags)

        except Exception as error:
            raise Exception(f"Error while calculating pitch! Error: {error}")

        # initializing structure logic
        input_dxgi_image: DXGIImage = self._init_dxgi_image(img_width, img_height, input_format_number, c_input_row_pitch.value, c_input_slice_pitch.value, image_data)
        output_dxgi_image: DXGIImage = self._init_dxgi_image(img_width, img_height, output_format_number, c_output_row_pitch.value, c_output_slice_pitch.value, b'')

        # decompressing image logic
        try:
            dll_file = ctypes.CDLL(dll_path)
            h_result = dll_file.DecompressBC(ctypes.byref(input_dxgi_image), ctypes.byref(output_dxgi_image))
        except Exception as error:
            raise Exception(f"Error while decoding compressed data! Error: {error}")

        if h_result != 0:
            raise Exception(f"DLL decompression failed! H_result: {h_result}")

        decoded_data_size: int = img_height * img_width * 4
        decoded_data = bytearray((c_uint8 * decoded_data_size).from_address(ctypes.addressof(output_dxgi_image.pixels.contents)))
        return decoded_data

    def decode_compressed_image_main(self, image_data: bytes, img_width: int, img_height: int, image_format: ImageFormats) -> bytes:
        """
        Main decoder function
        """
        return self._decode_directxtex_image(image_data, img_width, img_height, image_format)
