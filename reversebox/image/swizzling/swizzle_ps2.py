"""
Copyright © 2024  Bartłomiej Duda
License: GPL-3.0 License
"""

from reversebox.io_files.bytes_handler import BytesHandler


def unswizzle_ps2_palette(palette_data: bytes) -> bytes:
    unswizzled_palette_data: bytes = b""
    palette_handler = BytesHandler(palette_data)
    bytes_per_palette_pixel: int = 4
    parts: int = int(len(palette_data) / 32)
    stripes: int = 2
    colors: int = 8
    blocks: int = 2
    index: int = 0

    for part in range(parts):
        for block in range(blocks):
            for stripe in range(stripes):
                for color in range(colors):
                    palette_index: int = (
                        index
                        + part * colors * stripes * blocks
                        + block * colors
                        + stripe * stripes * colors
                        + color
                    )
                    palette_offset: int = palette_index * bytes_per_palette_pixel
                    palette_entry = palette_handler.get_bytes(
                        palette_offset, bytes_per_palette_pixel
                    )
                    unswizzled_palette_data += palette_entry

    return unswizzled_palette_data


def swizzle_ps2_palette(palette_data: bytes) -> bytes:
    return unswizzle_ps2_palette(
        palette_data
    )  # this function can both swizzle and unswizzle


# TODO - refactor this
def unswizzle_ps2_8bit(image_data: bytes, img_width: int, img_height: int) -> bytes:
    unswizzled_data: bytes = bytearray(img_width * img_height)
    for y in range(img_height):
        for x in range(img_width):
            block_location = (y & (~0xF)) * img_width + (x & (~0xF)) * 2
            swap_selector = (((y + 2) >> 2) & 0x1) * 4
            pos_y = (((y & (~3)) >> 1) + (y & 1)) & 0x7
            column_location = pos_y * img_width * 2 + ((x + swap_selector) & 0x7) * 4
            byte_num = ((y >> 1) & 1) + ((x >> 2) & 2)
            swizzle_id = block_location + column_location + byte_num
            unswizzled_data[y * img_width + x] = image_data[swizzle_id]  # type: ignore
    return unswizzled_data


# TODO - refactor this
def unswizzle_ps2_4bit(image_data: bytes, img_width: int, img_height: int) -> bytes:
    pixels: bytes = bytearray(img_width * img_height)
    for i in range(img_width * img_height // 2):
        index = image_data[i]
        id2 = (index >> 4) & 0xF
        id1 = index & 0xF
        pixels[i * 2] = id1  # type: ignore
        pixels[i * 2 + 1] = id2  # type: ignore
    new_pixels: bytes = unswizzle_ps2_8bit(pixels, img_width, img_height)
    unswizzled_data = bytearray(img_width * img_height)
    for i in range(img_width * img_height // 2):
        idx1 = new_pixels[i * 2 + 0]
        idx2 = new_pixels[i * 2 + 1]
        idx = ((idx2 << 4) | idx1) & 0xFF
        unswizzled_data[i] = idx
    return unswizzled_data
