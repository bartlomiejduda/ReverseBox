"""
Copyright © 2025  Bartłomiej Duda
License: GPL-3.0 License
"""

# Nintendo Switch Swizzling

# fmt: off


def _convert_switch(input_image_data: bytes, img_width: int, img_height: int,
                    bytes_per_block: int = 4, block_height: int = 8, width_pad: int = 8, height_pad: int = 8, swizzle_flag: bool = False):
    # set parameters
    converted_data = bytearray(len(input_image_data))
    if img_width % width_pad or img_height % height_pad:
        width_show = img_width
        height_show = img_height
        img_width = width_real = ((img_width + width_pad - 1) // width_pad) * width_pad
        img_height = height_real = ((img_height + height_pad - 1) // height_pad) * height_pad
    else:
        width_show = width_real = img_width
        height_show = height_real = img_height
    image_width_in_gobs = img_width * bytes_per_block // 64

    # unswizzling logic
    for Y in range(img_height):
        for X in range(img_width):
            Z = Y * img_width + X
            gob_address = 0 + (Y // (8 * block_height)) * 512 * block_height * image_width_in_gobs + (X * bytes_per_block // 64) * 512 * block_height + (Y % (8 * block_height) // 8) * 512
            X *= bytes_per_block
            address = gob_address + ((X % 64) // 32) * 256 + ((Y % 8) // 2) * 64 + ((X % 32) // 16) * 32 + (Y % 2) * 16 + (X % 16)
            if not swizzle_flag:
                converted_data[Z * bytes_per_block:(Z + 1) * bytes_per_block] = input_image_data[address:address + bytes_per_block]
            else:
                converted_data[address:address + bytes_per_block] = input_image_data[Z * bytes_per_block:(Z + 1) * bytes_per_block]

    # crop logic
    if width_show != width_real or height_show != height_real:
        crop = bytearray(width_show * height_show * bytes_per_block)
        for Y in range(height_show):
            offset_in = Y * width_real * bytes_per_block
            offset_out = Y * width_show * bytes_per_block
            if not swizzle_flag:
                crop[offset_out:offset_out + width_show * bytes_per_block] = converted_data[offset_in:offset_in + width_show * bytes_per_block]
            else:
                crop[offset_in:offset_in + width_show * bytes_per_block] = converted_data[offset_out:offset_out + width_show * bytes_per_block]
        converted_data = crop

    return converted_data


def unswizzle_switch(input_image_data: bytes, img_width: int, img_height: int,
                     bytes_per_block: int = 4, block_height: int = 8, width_pad: int = 8, height_pad: int = 8) -> bytes:
    return _convert_switch(input_image_data, img_width, img_height, bytes_per_block, block_height, width_pad, height_pad, False)


def swizzle_switch(input_image_data: bytes, img_width: int, img_height: int,
                   bytes_per_block: int = 4, block_height: int = 8, width_pad: int = 8, height_pad: int = 8) -> bytes:
    return _convert_switch(input_image_data, img_width, img_height, bytes_per_block, block_height, width_pad, height_pad, True)
