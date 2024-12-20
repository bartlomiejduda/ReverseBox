"""
Copyright © 2024  Bartłomiej Duda
License: GPL-3.0 License
"""

from reversebox.common.logger import get_logger

logger = get_logger(__name__)

# fmt: off

# TGA RLE compression
# https://www.dca.fee.unicamp.br/~martino/disciplinas/ea978/tgaffs.pdf


def decompress_rle_tga(image_data: bytes, bpp: int) -> bytes:
    bytes_per_pixel = bpp // 8
    decompressed_data: list[int] = []
    i = 0

    while i < len(image_data):
        header = image_data[i]
        i += 1

        packet_type = header & 0x80
        count = (header & 0x7F) + 1

        if packet_type:  # repeated packet
            pixel_data = image_data[i:i + bytes_per_pixel]
            i += bytes_per_pixel
            decompressed_data.extend(pixel_data * count)
        else:  # raw packet
            pixel_data = image_data[i:i + count * bytes_per_pixel]
            i += count * bytes_per_pixel
            decompressed_data.extend(pixel_data)

    return bytes(decompressed_data)


def compress_rle_tga(image_data: bytes, bpp: int) -> bytes:
    bytes_per_pixel = bpp // 8
    compressed_data: list[int] = []
    i = 0

    while i < len(image_data):

        # check for repeated pixels
        run_start = i
        run_length = 1
        while (i + bytes_per_pixel < len(image_data) and
               image_data[i:i + bytes_per_pixel] == image_data[i + bytes_per_pixel:i + 2 * bytes_per_pixel] and
               run_length < 128):
            run_length += 1
            i += bytes_per_pixel

        if run_length > 1:  # repeated packet
            compressed_data.append(0x80 | (run_length - 1))
            compressed_data.extend(image_data[run_start:run_start + bytes_per_pixel])
            i += bytes_per_pixel
        else:  # raw packet
            raw_start = i
            raw_length = 0
            while (i < len(image_data) and raw_length < 128 and
                   (i + bytes_per_pixel >= len(image_data) or
                    image_data[i:i + bytes_per_pixel] != image_data[i + bytes_per_pixel:i + 2 * bytes_per_pixel])):
                raw_length += 1
                i += bytes_per_pixel

            compressed_data.append(raw_length - 1)
            compressed_data.extend(image_data[raw_start:raw_start + raw_length * bytes_per_pixel])

    return bytes(compressed_data)
