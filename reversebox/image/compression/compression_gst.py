"""
Copyright © 2024  Bartłomiej Duda
License: GPL-3.0 License
"""

# fmt: off


# PS2 GS texture decompression
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

    if block_width == 4 and detail_bpp == 2:  # decompress GST 422
        for y in range(img_height):
            base_current_offset = (img_width // 4) * (y // block_height)
            for block_x in range(0, img_width, 4):
                detail_bits = detail_data[detail_current_offset]
                detail_current_offset += 1
                base_value = base_data[base_current_offset]
                base_current_offset += 1
                decompressed_texture_data[output_current_offset] = (base_value + ((detail_bits >> 0) & 3)) & 0xFF
                decompressed_texture_data[output_current_offset + 1] = (base_value + ((detail_bits >> 2) & 3)) & 0xFF
                decompressed_texture_data[output_current_offset + 2] = (base_value + ((detail_bits >> 4) & 3)) & 0xFF
                decompressed_texture_data[output_current_offset + 3] = (base_value + ((detail_bits >> 6) & 3)) & 0xFF
                output_current_offset += 4

    elif block_width == 2 and detail_bpp == 2:  # decompress GST 222
        for y in range(img_height):
            base_current_offset = (img_width // 2) * (y // block_height)
            for block_x in range(0, img_width, 4):
                detail_bits = detail_data[detail_current_offset]
                detail_current_offset += 1
                base_value = base_data[base_current_offset]
                base_current_offset += 1
                decompressed_texture_data[output_current_offset] = (base_value + ((detail_bits >> 0) & 3)) & 0xFF
                decompressed_texture_data[output_current_offset + 1] = (base_value + ((detail_bits >> 2) & 3)) & 0xFF
                base_value = base_data[base_current_offset]
                base_current_offset += 1
                decompressed_texture_data[output_current_offset + 2] = (base_value + ((detail_bits >> 4) & 3)) & 0xFF
                decompressed_texture_data[output_current_offset + 3] = (base_value + ((detail_bits >> 6) & 3)) & 0xFF
                output_current_offset += 4

    else:  # decompress other GST textures
        for y in range(img_height):
            if detail_bpp == 2:
                for block_x in range(0, img_width, 4):
                    for x in range(4):
                        base_current_offset = (img_width // block_width) * (y // block_height) + ((block_x + x) // block_width)
                        detail_value = detail_data[detail_current_offset]
                        base_value = base_data[base_current_offset]
                        calc_value = (detail_value >> (x * 2)) & 3
                        decompressed_texture_data[output_current_offset] = (base_value + calc_value) & 0xFF
                        output_current_offset += 1
                    detail_current_offset += 1

            else:
                for block_x in range(0, img_width, 8):
                    for x in range(8):
                        base_current_offset = (img_width // block_width) * (y // block_height) + ((block_x + x) // block_width)
                        detail_value = detail_data[detail_current_offset]
                        base_value = base_data[base_current_offset]
                        calc_value = (detail_value >> x) & 1
                        decompressed_texture_data[output_current_offset] = (base_value + calc_value) & 0xFF
                        output_current_offset += 1
                    detail_current_offset += 1

    return decompressed_texture_data
