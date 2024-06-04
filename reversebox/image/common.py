"""
Copyright © 2024  Bartłomiej Duda
License: GPL-3.0 License
"""


def convert_bpp_to_bytes_per_pixel(input_bpp: int) -> int:
    if input_bpp <= 8:
        return 1
    elif input_bpp <= 16:
        return 2
    elif input_bpp <= 24:
        return 3
    elif input_bpp <= 32:
        return 4
    else:
        raise Exception("Not supported bpp value!")


# The stride is the number of bytes from one row of pixels in memory to the next row of pixels in memory.
# Stride is also called pitch. If padding bytes are present, the stride is wider than the width of the image.
# stride = rowbytes = pitch
def get_stride_value(img_width: int, bpp: int) -> int:
    stride: int = img_width * bpp // 8
    return stride


# img_width = pixels_per_row
def get_img_width_from_stride(stride: int, bpp: int) -> int:
    img_width = stride * 8 // bpp
    return img_width
