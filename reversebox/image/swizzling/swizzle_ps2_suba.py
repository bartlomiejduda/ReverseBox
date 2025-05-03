"""
Copyright © 2025  Bartłomiej Duda
License: GPL-3.0 License
"""

# fmt: off


# PS2 ezSwizzle algorithm (Victor Suba swizzle)

# Used in:
# - ezSwizzle program


def _ps2_suba_swizzle_16bit(input_data: bytes, width: int, height: int, swizzle_flag: bool) -> bytes:
    converted_data: bytearray = bytearray(len(input_data))

    for y in range(height):
        for x in range(width):

            page_x = x & (~0x3f)
            page_y = y & (~0x3f)

            pages_horz = (width + 63) // 64
            pages_vert = (height + 63) // 64

            page_number = (page_y // 64) * pages_horz + (page_x // 64)

            page32_y = (page_number // pages_vert) * 32
            page32_x = (page_number % pages_vert) * 64

            page_location = (page32_y * height + page32_x) * 2

            loc_x = x & 0x3f
            loc_y = y & 0x3f

            block_location = (loc_x & (~0xf)) * height + (loc_y & (~0x7)) * 2
            column_location = ((y & 0x7) * height + (x & 0x7)) * 2

            short_num = (x >> 3) & 1  # 0 or 1

            dest_index = page_location + block_location + column_location + short_num

            if swizzle_flag:
                converted_data[dest_index] = input_data[y * width + x]
            else:
                converted_data[y * width + x] = input_data[dest_index]

    return converted_data


def _ps2_suba_swizzle_8bit(input_data: bytes, width: int, height: int, swizzle_flag: bool) -> bytes:
    converted_data: bytearray = bytearray(len(input_data))

    for y in range(height):
        for x in range(width):

            block_location = (y & (~0xf)) * width + (x & (~0xf)) * 2
            swap_selector = (((y + 2) >> 2) & 0x1) * 4
            posY = (((y & (~3)) >> 1) + (y & 1)) & 0x7
            column_location = posY * width * 2 + ((x + swap_selector) & 0x7) * 4

            byte_num = ((y >> 1) & 1) + ((x >> 2) & 2)  # 0,1,2,3

            index = block_location + column_location + byte_num
            if swizzle_flag:
                converted_data[index] = input_data[y * width + x]
            else:
                converted_data[y * width + x] = input_data[index]

    return converted_data


def _ps2_suba_swizzle_4bit(input_data: bytes, width: int, height: int, swizzle_flag: bool) -> bytes:
    converted_data = bytearray(len(input_data))

    for y in range(height):
        for x in range(width):
            index = y * width + x
            in_byte = input_data[index >> 1]
            u_pen = (in_byte >> ((index & 1) * 4)) & 0xF

            pageX = x & (~0x7F)
            pageY = y & (~0x7F)

            pages_horz = (width + 127) // 128
            pages_vert = (height + 127) // 128

            page_number = (pageY // 128) * pages_horz + (pageX // 128)

            page32Y = (page_number // pages_vert) * 32
            page32X = (page_number % pages_vert) * 64

            page_location = page32Y * height * 2 + page32X * 4

            locX = x & 0x7F
            locY = y & 0x7F

            block_location = ((locX & (~0x1F)) >> 1) * height + (locY & (~0xF)) * 2
            swap_selector = (((y + 2) >> 2) & 0x1) * 4
            posY = (((y & (~3)) >> 1) + (y & 1)) & 0x7

            column_location = posY * height * 2 + ((x + swap_selector) & 0x7) * 4

            byte_num = (x >> 3) & 3  # 0,1,2,3
            bits_set = (y >> 1) & 1  # 0, 1

            index_out = page_location + block_location + column_location + byte_num

            if swizzle_flag:
                out_byte = converted_data[index_out]
                out_byte = (out_byte & (~(0xF << (bits_set * 4)))) | (u_pen << (bits_set * 4))
                converted_data[index_out] = out_byte

            else:
                in_swiz_byte = input_data[index_out]
                u_pen_unswiz = (in_swiz_byte >> (bits_set * 4)) & 0xF
                out_index = index >> 1
                shift = (index & 1) * 4
                mask = 0xF << shift
                converted_data[out_index] = (converted_data[out_index] & (~mask)) | (u_pen_unswiz << shift)

    return converted_data
