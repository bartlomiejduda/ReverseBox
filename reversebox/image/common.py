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


# used in N64/WII games
def get_storage_wh(
    image_width: int, image_height: int, block_width: int, block_height: int
) -> tuple:
    image_width = (image_width + block_width - 1) // block_width * block_width
    image_height = (image_height + block_height - 1) // block_height * block_height
    return image_width, image_height


# used in N64/WII games
def crop_image(
    image_data: bytes,
    width: int,
    height: int,
    bpp: int,
    new_width: int,
    new_height: int,
) -> bytes:
    if width == new_width and height == new_height:
        return image_data

    cropped_image_data = bytearray(new_width * new_height * bpp // 8)

    lw = min(width, new_width) * bpp // 8

    for y in range(0, min(height, new_height)):
        dst = y * new_width * bpp // 8
        src = y * width * bpp // 8
        cropped_image_data[dst : dst + lw] = image_data[src : src + lw]

    return cropped_image_data
