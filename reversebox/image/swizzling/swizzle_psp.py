import struct


def unswizzle_psp(image_data: bytes, width: int, height: int, bpp: int) -> bytes:
    destination_offset: int = 0
    width = (width * bpp) >> 3
    destination = [0] * (width * height)
    row_blocks: int = width // 16
    magic_number: int = 8

    for y in range(height):
        for x in range(width):
            block_x = x // 16
            block_y = y // magic_number

            block_index = block_x + (block_y * row_blocks)
            block_address = block_index * 16 * magic_number
            offset: int = (
                block_address + (x - block_x * 16) + ((y - block_y * magic_number) * 16)
            )
            destination[destination_offset] = image_data[offset]
            destination_offset += 1

    result: bytes = b""
    for entry in destination:
        result += struct.pack("B", entry)

    return result


# TODO - verify/refactor this
def swizzle_psp(data, width: int, height: int):
    swizzled_data = [0] * (width * height)
    row_blocks = width // 16
    source_index = 0
    data = list(data)
    for y in range(height):
        for x in range(width):
            block_x = x // 16
            block_y = y // 8

            block_index = block_x + (block_y * row_blocks)
            block_address = block_index * 16 * 8
            swizzled_data[
                block_address + (x - (block_x * 16)) + ((y - (block_y * 8)) * 16)
            ] = data[source_index]
            source_index += 1
    return swizzled_data
