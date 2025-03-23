"""
Copyright © 2024-2025  Bartłomiej Duda
License: GPL-3.0 License
"""

from reversebox.image.common import convert_bpp_to_bytes_per_pixel

# Morton Order Texture Swizzling
# https://en.wikipedia.org/wiki/Z-order_curve
# Used in XBOX CLASSIC and PS3 games (e.g. EA XSH files)

# fmt: off


def calculate_morton_index(x: int, y: int, img_width: int, img_height: int) -> int:
    nx: int = 0
    ny: int = 0
    xpos: int = 0
    ypos: int = 0
    tpix: int = 1
    morton_index: int = y * img_width + x

    while tpix < img_width or tpix < img_height:
        if tpix < img_width:
            nx |= ((morton_index & 1) << xpos)
            xpos += 1
            morton_index >>= 1
        if tpix < img_height:
            ny |= ((morton_index & 1) << ypos)
            ypos += 1
            morton_index >>= 1
        tpix <<= 1

    morton_index = ny * img_width + nx
    return morton_index


def _convert_morton(image_data: bytes, img_width: int, img_height: int, bpp: int, swizzle_flag: bool) -> bytes:
    converted_data = bytearray(len(image_data))
    bytes_per_pixel: int = convert_bpp_to_bytes_per_pixel(bpp)
    source_index: int = 0

    for y in range(img_height):
        for x in range(img_width):
            morton_index = calculate_morton_index(x, y, img_width, img_height)
            destination_index = bytes_per_pixel * morton_index
            if not swizzle_flag:
                converted_data[destination_index: destination_index + bytes_per_pixel] = image_data[source_index: source_index + bytes_per_pixel]
            else:
                converted_data[source_index: source_index + bytes_per_pixel] = image_data[destination_index: destination_index + bytes_per_pixel]
            source_index += bytes_per_pixel

    return converted_data


def unswizzle_morton(image_data: bytes, img_width: int, img_height: int, bpp: int) -> bytes:
    return _convert_morton(image_data, img_width, img_height, bpp, False)


def swizzle_morton(image_data: bytes, img_width: int, img_height: int, bpp: int) -> bytes:
    return _convert_morton(image_data, img_width, img_height, bpp, True)


def calculate_morton_index_bc(t: int, width: int, height: int) -> int:
    num1 = num2 = 1
    num3 = t
    num4 = width
    num5 = height
    num6 = num7 = 0

    while num4 > 1 or num5 > 1:
        if num4 > 1:
            num6 += num2 * (num3 & 1)
            num3 >>= 1
            num2 *= 2
            num4 >>= 1
        if num5 > 1:
            num7 += num1 * (num3 & 1)
            num3 >>= 1
            num1 *= 2
            num5 >>= 1

    return num7 * width + num6


def _convert_morton_bc(pixel_data: bytes, img_width: int, img_height: int, bpp: int, block_width_height, swizzle_flag: bool) -> bytes:
    count: int = img_width * img_height * bpp // 8
    bytes_per_pixel: int = convert_bpp_to_bytes_per_pixel(bpp)
    block_data_size: int = bytes_per_pixel * block_width_height * block_width_height
    converted_data: bytearray = bytearray(count * 4)
    img_height //= block_width_height
    img_width //= block_width_height
    source_index: int = 0

    for t in range(img_width * img_height):
        index = calculate_morton_index_bc(t, img_width, img_height)
        destination_index = block_data_size * index
        if not swizzle_flag:
            converted_data[destination_index:destination_index + block_data_size] = pixel_data[source_index:source_index+block_data_size]
        else:
            converted_data[source_index:source_index+block_data_size] = pixel_data[destination_index:destination_index + block_data_size]
        source_index += block_data_size

    return converted_data


def unswizzle_morton_bc(pixel_data: bytes, img_width: int, img_height: int, bpp: int, block_width_height: int = 4) -> bytes:
    return _convert_morton_bc(pixel_data, img_width, img_height, bpp, block_width_height, False)


def swizzle_morton_bc(pixel_data: bytes, img_width: int, img_height: int, bpp: int, block_width_height: int = 4) -> bytes:
    return _convert_morton_bc(pixel_data, img_width, img_height, bpp, block_width_height, True)
