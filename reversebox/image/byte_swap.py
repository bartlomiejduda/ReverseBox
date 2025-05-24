"""
Copyright © 2025  Bartłomiej Duda
License: GPL-3.0 License
"""

# fmt: off

# Byte swapping functions


def swap_byte_order_x360(image_data: bytes) -> bytes:
    if len(image_data) % 2 != 0:
        raise Exception("Data size must be a multiple of 2 bytes!")

    swapped_data: bytearray = bytearray()
    for i in range(0, len(image_data), 2):
        group = image_data[i: i + 2]
        swapped_data.extend(group[::-1])
    return swapped_data


def swap_byte_order_gamecube(image_data: bytes, img_width: int, img_height: int) -> bytes:
    if len(image_data) % 8 != 0:
        raise ValueError("The data must be a multiple of 8 bytes (the size of one BC block)")

    bw: int = img_width // 4
    bh: int = img_height // 4
    block_size: int = 8
    tile_w: int = bw // 2
    tile_h: int = bh // 2
    tile_index: int = 0

    swapped_data: bytearray = bytearray(len(image_data))

    for ty in range(tile_h):
        for tx in range(tile_w):
            for by in range(2):
                for bx in range(2):
                    # Calculate destination position
                    dst_x = tx * 2 + bx
                    dst_y = ty * 2 + by
                    dst_index = (dst_y * bw + dst_x) * block_size

                    # Get source block and convert endianness
                    src_index = tile_index * block_size
                    block = image_data[src_index:src_index + block_size]

                    # Convert GameCube DXT1 to little-endian DXT1
                    # Swap color0 and color1 endianness
                    color0 = (block[0] << 8) | block[1]
                    color1 = (block[2] << 8) | block[3]

                    # Reorder 2-bit indices (bit reversal within each byte)
                    indices = bytearray(4)
                    for i in range(4):
                        b = block[4 + i]
                        indices[i] = ((b & 0b00000011) << 6) | \
                                     ((b & 0b00001100) << 2) | \
                                     ((b & 0b00110000) >> 2) | \
                                     ((b & 0b11000000) >> 6)

                    # Write converted block to output
                    swapped_data[dst_index] = color0 & 0xff
                    swapped_data[dst_index + 1] = color0 >> 8
                    swapped_data[dst_index + 2] = color1 & 0xff
                    swapped_data[dst_index + 3] = color1 >> 8
                    swapped_data[dst_index + 4:dst_index + 8] = indices

                    tile_index += 1

    return bytes(swapped_data)
