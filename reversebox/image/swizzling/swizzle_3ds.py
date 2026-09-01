"""
Copyright © 2024-2025  Bartłomiej Duda
License: GPL-3.0 License
"""

from reversebox.image.swizzling.morton_index import calculate_morton_index

# Nintendo 3DS Swizzling
# Can occur in:
# - some MT Framework games on 3DS
# - "Mario & Luigi: Superstar Saga + Bowser's Minions" (3DS)
# - BFLIM image files

# fmt: off


def _convert_3ds_blocks(image_data: bytes, img_width: int, img_height: int, bpp: int,
                        block_width: int, block_height: int, swizzle_flag: bool) -> bytes:
    """Convert block-compressed data using the 3DS 8x8-pixel tile order."""
    tile_width: int = 8
    tile_height: int = 8

    if block_width <= 0 or block_height <= 0:
        raise ValueError("Block dimensions must be positive!")
    if tile_width % block_width != 0 or tile_height % block_height != 0:
        raise ValueError("3DS block dimensions must divide an 8x8-pixel tile!")
    if img_width % tile_width != 0 or img_height % tile_height != 0:
        raise ValueError("3DS image dimensions must be multiples of 8 pixels!")

    block_data_size: int = block_width * block_height * bpp // 8
    if block_data_size <= 0:
        raise ValueError("Block data size must be at least one byte!")

    blocks_per_row: int = img_width // block_width
    blocks_per_column: int = img_height // block_height
    tile_blocks_w: int = tile_width // block_width
    tile_blocks_h: int = tile_height // block_height
    expected_size: int = blocks_per_row * blocks_per_column * block_data_size
    if len(image_data) != expected_size:
        raise ValueError(f"Expected {expected_size} bytes, got {len(image_data)}!")

    converted_data: bytearray = bytearray(expected_size)
    source_offset: int = 0

    for tile_y in range(0, blocks_per_column, tile_blocks_h):
        for tile_x in range(0, blocks_per_row, tile_blocks_w):
            for tile_block in range(tile_blocks_w * tile_blocks_h):
                morton_block: int = calculate_morton_index(tile_block, tile_blocks_w, tile_blocks_h)
                block_x: int = morton_block % tile_blocks_w
                block_y: int = morton_block // tile_blocks_w
                destination_block: int = (tile_y + block_y) * blocks_per_row + tile_x + block_x
                destination_offset: int = destination_block * block_data_size
                if not swizzle_flag:
                    converted_data[destination_offset:destination_offset + block_data_size] = \
                        image_data[source_offset:source_offset + block_data_size]
                else:
                    converted_data[source_offset:source_offset + block_data_size] = \
                        image_data[destination_offset:destination_offset + block_data_size]
                source_offset += block_data_size

    return bytes(converted_data)


def _convert_3ds(image_data: bytes, img_width: int, img_height: int, bpp: int, swizzle_flag: bool) -> bytes:
    l: int = 8
    m: int = 4
    s: int = 2
    strip_size: int = bpp * s // 8

    converted_data = bytearray(img_width * img_height * bpp // 8)
    ptr: int = 0

    for y in range(0, img_height, l):
        for x in range(0, img_width, l):
            for y1 in range(0, l, m):
                for x1 in range(0, l, m):
                    for y2 in range(0, m, s):
                        for x2 in range(0, m, s):
                            for y3 in range(s):
                                idx = (((y + y1 + y2 + y3) * img_width) + x + x1 + x2) * bpp // 8
                                if not swizzle_flag:
                                    converted_data[idx: idx+strip_size] = image_data[ptr: ptr + strip_size]
                                else:
                                    converted_data[ptr: ptr+strip_size] = image_data[idx: idx + strip_size]
                                ptr += strip_size

    return converted_data


def unswizzle_3ds(image_data: bytes, img_width: int, img_height: int, bpp: int) -> bytes:
    return _convert_3ds(image_data, img_width, img_height, bpp, False)


def swizzle_3ds(image_data: bytes, img_width: int, img_height: int, bpp: int) -> bytes:
    return _convert_3ds(image_data, img_width, img_height, bpp, True)


def unswizzle_3ds_blocks(image_data: bytes, img_width: int, img_height: int, bpp: int,
                         block_width: int, block_height: int) -> bytes:
    return _convert_3ds_blocks(
        image_data, img_width, img_height, bpp, block_width, block_height, False
    )


def swizzle_3ds_blocks(image_data: bytes, img_width: int, img_height: int, bpp: int,
                       block_width: int, block_height: int) -> bytes:
    return _convert_3ds_blocks(
        image_data, img_width, img_height, bpp, block_width, block_height, True
    )
