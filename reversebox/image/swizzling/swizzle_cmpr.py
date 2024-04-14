# TODO - refactor this
# https://wiki.tockdom.com/wiki/Image_Formats#CMPR
def unswizzle_cmpr(pixel_data, width, height):
    tile_width = 2
    tile_height = 2
    dxt_block_size = 8

    num_block_width = width // 8
    num_block_height = height // 8

    tile_size = tile_width * tile_height * dxt_block_size
    line_size = tile_width * dxt_block_size

    unswizzled_data = bytearray(len(pixel_data))

    for y in range(0, num_block_height):
        for x in range(0, num_block_width):
            data_ptr = (y * num_block_width + x) * tile_size
            for ty in range(0, tile_height):
                cur_height = y * tile_height + ty
                dst_index = (cur_height * num_block_width + x) * line_size
                src_index = data_ptr + ty * line_size
                for p in range(tile_width):
                    unswizzled_data[dst_index + p * dxt_block_size] = pixel_data[
                        src_index + p * dxt_block_size + 1
                    ]
                    unswizzled_data[dst_index + p * dxt_block_size + 1] = pixel_data[
                        src_index + p * dxt_block_size
                    ]
                    unswizzled_data[dst_index + p * dxt_block_size + 2] = pixel_data[
                        src_index + p * dxt_block_size + 3
                    ]
                    unswizzled_data[dst_index + p * dxt_block_size + 3] = pixel_data[
                        src_index + p * dxt_block_size + 2
                    ]
                    for i in range(4, 8):
                        index = pixel_data[src_index + p * dxt_block_size + i]
                        swap_index = (
                            ((index >> 6) & 0x3)
                            | (((index >> 4) & 0x3) << 2)
                            | (((index >> 2) & 0x3) << 4)
                            | ((index & 0x3) << 6)
                        )
                        unswizzled_data[dst_index + p * dxt_block_size + i] = swap_index

    return unswizzled_data
