"""
Copyright © 2024-2025  Bartłomiej Duda
License: GPL-3.0 License
"""

# fmt: off

from reversebox.image.common import get_stride_value_psp


def psp_image_padding(
    image_data: bytes, img_width: int, img_height: int, bpp: int
) -> bytes:
    padded_data_offset: int = 0
    stride: int = get_stride_value_psp(img_width, bpp)

    if bpp >= 8:
        bytes_per_pixel: int = bpp // 8
        padded_data = bytearray(img_width * img_height * bytes_per_pixel)
        for y in range(img_height):
            row_start = y * stride
            row_end = row_start + img_width * bytes_per_pixel
            padded_data[padded_data_offset: padded_data_offset + img_width * bytes_per_pixel] = image_data[row_start:row_end]
            padded_data_offset += img_width * bytes_per_pixel
    elif bpp == 4:
        padded_data = bytearray(img_width * img_height // 2)
        for y in range(img_height):
            row_start = y * stride
            row_end = row_start + img_width // 2
            padded_data[padded_data_offset: padded_data_offset + img_width // 2] = (image_data[row_start:row_end])
            padded_data_offset += img_width // 2
    else:
        raise Exception(f"Not supported bpp={bpp}")

    return padded_data
