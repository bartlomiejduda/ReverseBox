"""
Copyright © 2024  Bartłomiej Duda
License: GPL-3.0 License
"""


def decompress_gst_image(
    base_data: bytes,
    detail_data: bytes,
    img_width: int,
    img_height: int,
    block_width: int,
    block_height: int,
    detail_bpp: int,
):
    decompressed_texture_data = bytearray(img_width * img_height)
    detail_current_offset: int = 0
    output_current_offset: int = 0
    if block_width == 4 and detail_bpp == 2:
        for y in range(img_height):
            base_current_offset = (img_width // 4) * (y // block_height)
            for x in range(0, img_width, 4):
                detail_bits = detail_data[detail_current_offset]
                detail_current_offset += 1
                base_value = base_data[base_current_offset]
                base_current_offset += 1
                decompressed_texture_data[output_current_offset] = base_value + (
                    (detail_bits >> 0) & 3
                )
                decompressed_texture_data[output_current_offset + 1] = base_value + (
                    (detail_bits >> 2) & 3
                )
                decompressed_texture_data[output_current_offset + 2] = base_value + (
                    (detail_bits >> 4) & 3
                )
                decompressed_texture_data[output_current_offset + 3] = base_value + (
                    (detail_bits >> 6) & 3
                )
                output_current_offset += 4

    elif block_width == 2 and detail_bpp == 2:
        pass  # TODO

    else:
        pass  # TODO

    return decompressed_texture_data
