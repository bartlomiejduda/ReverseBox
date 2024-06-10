"""
Copyright © 2024  Bartłomiej Duda
License: GPL-3.0 License
"""
from reversebox.image.common import convert_bpp_to_bytes_per_pixel

# Swizzling used in GameCube and WII games

# fmt: off


def get_pixel_offset_bpp32(x: int, y: int, img_width: int) -> int:
    number_of_blocks_x = (3 + img_width) >> 2
    x_block = x >> 2
    y_block = y >> 2
    x_pix = x & 3
    y_pix = y & 3
    offset = ((y_block*number_of_blocks_x + x_block) << 6) + ((y_pix << 3) + (x_pix << 1))
    return offset


def get_pixel_offset_bpp16(x: int, y: int, img_width: int) -> int:
    number_of_blocks_x = (3 + img_width) >> 2
    x_block = x >> 2
    y_block = y >> 2
    x_pix = x & 3
    y_pix = y & 3
    offset = ((y_block*number_of_blocks_x + x_block) << 5) + ((y_pix << 3) + (x_pix << 1))
    return offset


def get_pixel_offset_bpp8(x: int, y: int, img_width: int) -> int:
    number_of_blocks_x = (7 + img_width) >> 3
    x_block = x >> 3
    y_block = y >> 2
    x_pix = x & 7
    y_pix = y & 3
    offset = ((y_block*number_of_blocks_x + x_block) << 5) + ((y_pix << 3) + x_pix)
    return offset


def get_pixel_offset_bpp4(x: int, y: int, img_width: int) -> int:
    number_of_blocks_x = (7 + img_width) >> 3
    x_block = x >> 3
    y_block = y >> 3
    x_pix = x & 7
    y_pix = y & 7
    offset = ((y_block*number_of_blocks_x + x_block) << 5) + ((y_pix << 2) + (x_pix >> 1))
    return offset


def get_pixel_offset(x: int, y: int, img_width: int, bpp: int) -> int:
    if bpp == 32:
        return get_pixel_offset_bpp32(x, y, img_width)
    elif bpp in (15, 16):
        return get_pixel_offset_bpp16(x, y, img_width)
    elif bpp == 8:
        return get_pixel_offset_bpp8(x, y, img_width)
    elif bpp == 4:
        return get_pixel_offset_bpp4(x, y, img_width)
    else:
        raise Exception("Bpp not supported!")


def unswizzle_gamecube(image_data: bytes, img_width: int, img_height: int, bpp: int) -> bytes:
    unswizzled_data = bytearray(len(image_data))
    destination_index: int = 0
    bytes_per_pixel: int = convert_bpp_to_bytes_per_pixel(bpp)

    for y in range(img_height):
        for x in range(img_width):
            index = get_pixel_offset(x, y, img_width, bpp)

            if bpp == 32:
                unswizzled_data[destination_index] = image_data[index]
                unswizzled_data[destination_index+1] = image_data[index+1]
                unswizzled_data[destination_index+2] = image_data[index+32]
                unswizzled_data[destination_index+3] = image_data[index+33]
                destination_index += 4
            else:
                unswizzled_data[destination_index: destination_index + bytes_per_pixel] = image_data[index: index + bytes_per_pixel]
                destination_index += bytes_per_pixel

    return unswizzled_data
