"""
Copyright © 2024  Bartłomiej Duda
License: GPL-3.0 License
"""
from reversebox.image.common import convert_bpp_to_bytes_per_pixel
from reversebox.image.swizzling.swizzle_morton import calculate_morton_index

# fmt: off

# Swizzle used in PS4 games e.g. "Dragons Dogma Dark Arisen"


# TODO - rewrite this
def unswizzle_ps4(image_data: bytes, img_width: int, img_height: int, bpp: int) -> bytes:
    unswizzled_data = bytearray(len(image_data))
    bytes_per_pixel: int = convert_bpp_to_bytes_per_pixel(bpp)
    block_size: int = bytes_per_pixel * 16
    source_index: int = 0
    img_height //= 4
    img_width //= 4

    for y in range((img_height + 7) // 8):
        for x in range((img_width + 7) // 8):
            for t in range(64):
                morton_index = calculate_morton_index(t, 8, 8)
                data_y = morton_index // 8
                data_x = morton_index % 8
                if x * 8 + data_x < img_width and y * 8 + data_y < img_height:
                    destination_index = block_size * ((y * 8 + data_y) * img_width + x * 8 + data_x)
                    unswizzled_data[destination_index: destination_index + block_size] = image_data[source_index: source_index + block_size]
                    source_index += block_size

    return unswizzled_data
