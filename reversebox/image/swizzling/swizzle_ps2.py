from reversebox.io_files.bytes_handler import BytesHandler


def unswizzle_ps2_palette(palette_data: bytes) -> bytes:
    converted_raw_palette_data: bytes = b""
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
                    pal_index: int = (
                        index
                        + part * colors * stripes * blocks
                        + block * colors
                        + stripe * stripes * colors
                        + color
                    )
                    pal_offset: int = pal_index * bytes_per_palette_pixel
                    pal_entry = palette_handler.get_bytes(
                        pal_offset, bytes_per_palette_pixel
                    )
                    converted_raw_palette_data += pal_entry

    return converted_raw_palette_data


# TODO - refactor this
def unswizzle_ps2_8bit(buffer, width, height):
    unswizzled_data = bytearray(width * height)
    for y in range(height):
        for x in range(width):
            block_location = (y & (~0xF)) * width + (x & (~0xF)) * 2
            swap_selector = (((y + 2) >> 2) & 0x1) * 4
            pos_y = (((y & (~3)) >> 1) + (y & 1)) & 0x7
            column_location = pos_y * width * 2 + ((x + swap_selector) & 0x7) * 4
            byte_num = ((y >> 1) & 1) + ((x >> 2) & 2)
            swizzle_id = block_location + column_location + byte_num
            unswizzled_data[y * width + x] = buffer[swizzle_id]
    return unswizzled_data


# TODO - refactor this
def unswizzle_ps2_4bit(buffer, width, height):
    pixels = bytearray(width * height)
    for i in range(width * height // 2):
        index = buffer[i]
        id2 = (index >> 4) & 0xF
        id1 = index & 0xF
        pixels[i * 2] = id1
        pixels[i * 2 + 1] = id2
    new_pixels = unswizzle_ps2_8bit(pixels, width, height)
    unswizzled_data = bytearray(width * height)
    for i in range(width * height // 2):
        idx1 = new_pixels[i * 2 + 0]
        idx2 = new_pixels[i * 2 + 1]
        idx = ((idx2 << 4) | idx1) & 0xFF
        unswizzled_data[i] = idx
    return unswizzled_data
