# Thanks to Vee from Xentax discord server
# for this contribution

# TODO - write some tests
# TODO - verify with this http://homebrew.pixelbath.com/wiki/PSP_texture_swizzling
# TODO - and this https://github.com/nickworonekin/puyotools/blob/a949eb452e4743b94517ca08e720759cc0381a25/src/PuyoTools.Core/Textures/Gim/GimTextureDecoder.cs#L333


def psp_swizzle(data, width: int, height: int):
    result = [0] * (width * height)
    row_blocks = width // 16
    source_index = 0
    data = list(data)
    for y in range(height):
        for x in range(width):
            block_x = x // 16
            block_y = y // 8

            block_index = block_x + (block_y * row_blocks)
            block_address = block_index * 16 * 8
            result[
                block_address + (x - (block_x * 16)) + ((y - (block_y * 8)) * 16)
            ] = data[source_index]
            source_index += 1
    return result


def psp_unswizzle(data, width: int, height: int):
    result = [0] * (width * height)
    row_blocks = width // 16
    index = 0
    data = list(data)
    for y in range(height):
        for x in range(width):
            block_x = x // 16
            block_y = y // 8

            block_index = block_x + (block_y * row_blocks)
            block_address = block_index * 16 * 8
            data[index] = result[
                block_address + (x - (block_x * 16)) + ((y - (block_y * 8)) * 16)
            ]
            index += 1
    return result
