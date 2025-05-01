"""
Copyright © 2025  Bartłomiej Duda
License: GPL-3.0 License
"""

# fmt: off


# PS2 4-bit swizzle algorithm
# special "type 3" 4-bit swizzle/unswizzle function
# Used in:
# - EA Games (e.g. SSH files from Cricket 2005 (PS2))
# - BloodRayne 1 (PS2)


import numpy as np

PSMT8_PAGE_WIDTH = 128
PSMT8_PAGE_HEIGHT = 64
PSMCT32_PAGE_WIDTH = 64
PSMCT32_PAGE_HEIGHT = 32
PSMT4_PAGE_WIDTH = 128
PSMT4_PAGE_HEIGHT = 128
PSMT4_BLOCK_WIDTH = 32
PSMT4_BLOCK_HEIGHT = 16
PSMT8_BLOCK_WIDTH = 16
PSMT8_BLOCK_HEIGHT = 16
PSMCT32_BLOCK_WIDTH = 8
PSMCT32_BLOCK_HEIGHT = 8


def _unswizzle4_convert_block(input_block_data: bytes) -> bytes:
    assert len(input_block_data) == 256
    unswizzle_lut_table = np.array([
        0, 8, 16, 24, 32, 40, 48, 56,
        2, 10, 18, 26, 34, 42, 50, 58,
        4, 12, 20, 28, 36, 44, 52, 60,
        6, 14, 22, 30, 38, 46, 54, 62,
        64, 72, 80, 88, 96, 104, 112, 120,
        66, 74, 82, 90, 98, 106, 114, 122,
        68, 76, 84, 92, 100, 108, 116, 124,
        70, 78, 86, 94, 102, 110, 118, 126,
        33, 41, 49, 57, 1, 9, 17, 25,
        35, 43, 51, 59, 3, 11, 19, 27,
        37, 45, 53, 61, 5, 13, 21, 29,
        39, 47, 55, 63, 7, 15, 23, 31,
        97, 105, 113, 121, 65, 73, 81, 89,
        99, 107, 115, 123, 67, 75, 83, 91,
        101, 109, 117, 125, 69, 77, 85, 93,
        103, 111, 119, 127, 71, 79, 87, 95,
        32, 40, 48, 56, 0, 8, 16, 24,
        34, 42, 50, 58, 2, 10, 18, 26,
        36, 44, 52, 60, 4, 12, 20, 28,
        38, 46, 54, 62, 6, 14, 22, 30,
        96, 104, 112, 120, 64, 72, 80, 88,
        98, 106, 114, 122, 66, 74, 82, 90,
        100, 108, 116, 124, 68, 76, 84, 92,
        102, 110, 118, 126, 70, 78, 86, 94,
        1, 9, 17, 25, 33, 41, 49, 57,
        3, 11, 19, 27, 35, 43, 51, 59,
        5, 13, 21, 29, 37, 45, 53, 61,
        7, 15, 23, 31, 39, 47, 55, 63,
        65, 73, 81, 89, 97, 105, 113, 121,
        67, 75, 83, 91, 99, 107, 115, 123,
        69, 77, 85, 93, 101, 109, 117, 125,
        71, 79, 87, 95, 103, 111, 119, 127
    ], dtype=np.uint8)

    output_block_data: bytearray = bytearray(16 * 16)
    index1: int = 0
    p_in: int = 0
    for k in range(4):
        index0 = (k % 2) * 128

        for i in range(16):
            for j in range(4):
                c_out = 0x00
                i0 = unswizzle_lut_table[index0]
                index0 += 1
                i1 = i0 // 2
                i2 = (i0 & 0x1) * 4
                c_in = (input_block_data[p_in + i1] & (0x0F << i2)) >> i2
                c_out = c_out | c_in

                i0 = unswizzle_lut_table[index0]
                index0 += 1
                i1 = i0 // 2
                i2 = (i0 & 0x1) * 4
                c_in = (input_block_data[p_in + i1] & (0x0F << i2)) >> i2
                c_out = c_out | (c_in << 4) & 0xF0

                output_block_data[index1] = c_out
                index1 += 1
        p_in += 64

    assert len(output_block_data) == 256
    return output_block_data


def _unswizzle4_convert_page(width: int, height: int, input_page_data: bytes) -> bytes:
    block_table4 = np.array([
        0, 2, 8, 10, 1, 3, 9, 11, 4, 6, 12, 14, 5, 7, 13, 15,
        16, 18, 24, 26, 17, 19, 25, 27, 20, 22, 28, 30, 21, 23, 29, 31
    ], dtype=np.uint32)

    block_table32 = np.array([
        0, 1, 4, 5, 16, 17, 20, 21, 2, 3, 6, 7, 18, 19, 22, 23,
        8, 9, 12, 13, 24, 25, 28, 29, 10, 11, 14, 15, 26, 27, 30, 31
    ], dtype=np.uint32)

    output_page_data: bytearray = bytearray(PSMCT32_PAGE_WIDTH * 4 * PSMCT32_PAGE_HEIGHT)

    index32_h_arr = np.zeros(32, dtype=np.uint32)
    index32_v_arr = np.zeros(32, dtype=np.uint32)

    index0: int = 0
    for i in range(4):
        for j in range(8):
            index1 = block_table32[index0]
            index32_h_arr[index1] = j
            index32_v_arr[index1] = i
            index0 += 1

    n_width = width // 32
    n_height = height // 16
    input_page_line_size = 256
    output_page_line_size = 128 // 2

    for i in range(n_height):
        for j in range(n_width):
            in_block_nb = block_table4[i * n_width + j]
            po0 = bytearray(16 * 16)
            po1_offset = 8 * index32_v_arr[in_block_nb] * input_page_line_size + index32_h_arr[in_block_nb] * 32
            po1 = input_page_data[po1_offset:]

            for k in range(PSMCT32_BLOCK_HEIGHT):
                po0[k*32:(k+1)*32] = po1[k*input_page_line_size:k*input_page_line_size + 32]

            output_block = _unswizzle4_convert_block(po0)

            for k in range(PSMT4_BLOCK_HEIGHT):
                start = (16 * i * output_page_line_size) + j * 16 + k * output_page_line_size
                output_page_data[start:start + 16] = output_block[k*16:k*16 + 16]

    return output_page_data


def ea_unswizzle4(input_data: bytes, img_width: int, img_height: int) -> bytes:
    output_data: bytearray = bytearray(len(input_data))
    n_page_w: int = (img_width - 1) // PSMT4_PAGE_WIDTH + 1
    n_page_h: int = (img_height - 1) // PSMT4_PAGE_HEIGHT + 1
    n_page4_width_byte: int = PSMT4_PAGE_WIDTH // 2
    n_page32_width_byte: int = PSMCT32_PAGE_WIDTH * 4

    if n_page_h == 1:
        n_input_width_byte = img_height * 2
        n_output_height = img_height
    else:
        n_input_width_byte = n_page32_width_byte
        n_output_height = PSMT4_PAGE_HEIGHT

    if n_page_w == 1:
        n_input_height = img_width // 4
        n_output_width_byte = img_width // 2
    else:
        n_input_height = PSMCT32_PAGE_HEIGHT
        n_output_width_byte = n_page4_width_byte

    for i in range(n_page_h):
        for j in range(n_page_w):
            po0_offset = (n_input_width_byte * n_input_height) * n_page_w * i + n_input_width_byte * j
            po0 = input_data[po0_offset:]
            input_page = bytearray(PSMT4_PAGE_WIDTH // 2 * PSMT4_PAGE_HEIGHT)

            for k in range(n_input_height):
                src_offset = k * n_input_width_byte * n_page_w
                dst_offset = k * n_page32_width_byte
                input_page[dst_offset:dst_offset + n_input_width_byte] = po0[src_offset:src_offset + n_input_width_byte]

            output_page = _unswizzle4_convert_page(PSMT4_PAGE_WIDTH, PSMT4_PAGE_HEIGHT, input_page)

            pi0_offset = (n_output_width_byte * n_output_height) * n_page_w * i + n_output_width_byte * j
            for k in range(n_output_height):
                src_offset = k * n_page4_width_byte
                dst_offset = pi0_offset + k * n_output_width_byte * n_page_w
                output_data[dst_offset:dst_offset + n_output_width_byte] = output_page[src_offset:src_offset + n_output_width_byte]

    return output_data


def _swizzle4_convert_block(input_block_data: bytes) -> bytes:
    assert len(input_block_data) == 256
    swizzle4_lut_table = np.array([
        0, 68, 8,  76, 16, 84, 24, 92,
        1, 69, 9,  77, 17, 85, 25, 93,
        2, 70, 10, 78, 18, 86, 26, 94,
        3, 71, 11, 79, 19, 87, 27, 95,
        4, 64, 12, 72, 20, 80, 28, 88,
        5, 65, 13, 73, 21, 81, 29, 89,
        6, 66, 14, 74, 22, 82, 30, 90,
        7, 67, 15, 75, 23, 83, 31, 91,
        32, 100, 40, 108, 48, 116, 56, 124,
        33, 101, 41, 109, 49, 117, 57, 125,
        34, 102, 42, 110, 50, 118, 58, 126,
        35, 103, 43, 111, 51, 119, 59, 127,
        36, 96,  44, 104, 52, 112, 60, 120,
        37, 97,  45, 105, 53, 113, 61, 121,
        38, 98,  46, 106, 54, 114, 62, 122,
        39, 99,  47, 107, 55, 115, 63, 123,
        4, 64, 12, 72, 20, 80, 28, 88,
        5, 65, 13, 73, 21, 81, 29, 89,
        6, 66, 14, 74, 22, 82, 30, 90,
        7, 67, 15, 75, 23, 83, 31, 91,
        0, 68, 8,  76, 16, 84, 24, 92,
        1, 69, 9,  77, 17, 85, 25, 93,
        2, 70, 10, 78, 18, 86, 26, 94,
        3, 71, 11, 79, 19, 87, 27, 95,
        36, 96,  44, 104, 52, 112, 60, 120,
        37, 97,  45, 105, 53, 113, 61, 121,
        38, 98,  46, 106, 54, 114, 62, 122,
        39, 99,  47, 107, 55, 115, 63, 123,
        32, 100, 40, 108, 48, 116, 56, 124,
        33, 101, 41, 109, 49, 117, 57, 125,
        34, 102, 42, 110, 50, 118, 58, 126,
        35, 103, 43, 111, 51, 119, 59, 127
    ], dtype=np.uint8)
    output_block_data: bytearray = bytearray(16 * 16)

    index1: int = 0
    p_in: int = 0
    for k in range(4):
        index0 = (k % 2) * 128
        for i in range(16):
            for j in range(4):
                c_out = 0x00
                for step in range(2):
                    i0 = swizzle4_lut_table[index0]
                    index0 += 1
                    i1 = i0 // 2
                    i2 = (i0 & 0x1) * 4
                    c_in = (input_block_data[p_in + i1] & (0x0f << i2)) >> i2
                    if step == 0:
                        c_out |= c_in
                    else:
                        c_out |= (c_in << 4) & 0xf0
                output_block_data[index1] = c_out
                index1 += 1
        p_in += 64

    assert len(output_block_data) == 256
    return output_block_data


def _swizzle4_convert_page(width: int, height: int, input_page_data: bytes) -> bytes:
    block_table4 = np.array([
         0,  2,  8, 10, 1,  3,  9, 11,
         4,  6, 12, 14, 5,  7, 13, 15,
         16, 18, 24, 26, 17, 19, 25, 27,
         20, 22, 28, 30, 21, 23, 29, 31
    ], dtype=np.uint32)

    block_table32 = np.array([
         0,  1,  4,  5, 16, 17, 20, 21,
         2,  3,  6,  7, 18, 19, 22, 23,
         8,  9, 12, 13, 24, 25, 28, 29,
         10, 11, 14, 15, 26, 27, 30, 31
    ], dtype=np.uint32)

    index32_h = np.zeros(32, dtype=np.uint32)
    index32_v = np.zeros(32, dtype=np.uint32)
    output_page_data = bytearray(PSMCT32_PAGE_WIDTH * 4 * PSMCT32_PAGE_HEIGHT)

    index0: int = 0
    for i in range(4):
        for j in range(8):
            index1 = block_table32[index0]
            index32_h[index1] = j
            index32_v[index1] = i
            index0 += 1

    n_width = width // 32
    n_height = height // 16
    input_page_line_size = 128 // 2
    output_page_line_size = 256

    input_block: bytearray = bytearray(16 * 16)

    for i in range(n_height):
        for j in range(n_width):
            pi0 = input_block
            pi1_idx = 16 * i * input_page_line_size + j * 16

            in_block_nb = block_table4[i * n_width + j]

            for k in range(PSMT4_BLOCK_HEIGHT):
                start = pi1_idx + k * input_page_line_size
                pi0[k * (PSMT4_BLOCK_WIDTH // 2):(k + 1) * (PSMT4_BLOCK_WIDTH // 2)] = input_page_data[start:start + (PSMT4_BLOCK_WIDTH // 2)]

            output_block = _swizzle4_convert_block(input_block)

            po0_idx = 8 * index32_v[in_block_nb] * output_page_line_size + index32_h[in_block_nb] * 32

            for k in range(PSMCT32_BLOCK_HEIGHT):
                start = k * PSMCT32_BLOCK_WIDTH * 4
                end = start + PSMCT32_BLOCK_WIDTH * 4
                out_start = po0_idx + k * output_page_line_size
                output_page_data[out_start:out_start + PSMCT32_BLOCK_WIDTH * 4] = output_block[start:end]

    return output_page_data


def ea_swizzle4(input_data: bytes, width: int, height: int) -> bytes:
    output_data: bytearray = bytearray(len(input_data))
    n_page_w: int = (width - 1) // PSMT4_PAGE_WIDTH + 1
    n_page_h: int = (height - 1) // PSMT4_PAGE_HEIGHT + 1
    n_page4_width_byte: int = PSMT4_PAGE_WIDTH // 2
    n_page32_width_byte: int = PSMCT32_PAGE_WIDTH * 4

    if n_page_w == 1:
        n_input_width_byte = width // 2
        n_output_height = width // 4
    else:
        n_input_width_byte = n_page4_width_byte
        n_output_height = PSMCT32_PAGE_HEIGHT

    if n_page_h == 1:
        n_input_height = height
        n_output_width_byte = height * 2
    else:
        n_input_height = PSMT4_PAGE_HEIGHT
        n_output_width_byte = n_page32_width_byte

    input_page: bytearray = bytearray(PSMT4_PAGE_WIDTH // 2 * PSMT4_PAGE_HEIGHT)

    for i in range(n_page_h):
        for j in range(n_page_w):
            for k in range(n_input_height):
                src_idx = (n_input_width_byte * n_input_height) * n_page_w * i + n_input_width_byte * j + k * n_input_width_byte * n_page_w
                dst_idx = k * n_page4_width_byte
                input_page[dst_idx:dst_idx + n_input_width_byte] = input_data[src_idx:src_idx + n_input_width_byte]

            output_page = _swizzle4_convert_page(PSMT4_PAGE_WIDTH, PSMT4_PAGE_HEIGHT, input_page)

            for k in range(n_output_height):
                src_idx = k * n_page32_width_byte
                dst_idx = (n_output_width_byte * n_output_height) * n_page_w * i + n_output_width_byte * j + k * n_output_width_byte * n_page_w
                output_data[dst_idx:dst_idx + n_output_width_byte] = output_page[src_idx:src_idx + n_output_width_byte]

    return output_data
