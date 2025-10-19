"""
Copyright © 2024  Bartłomiej Duda
License: GPL-3.0 License
"""

from reversebox.common.logger import get_logger

logger = get_logger(__name__)

# fmt: off

# PackBits (Macintosh RLE) compression
# Used in TIFF and PSD files


def decompress_packbits(image_data: bytes) -> bytes:
    """
    Decompresses the input bytes using the PackBits algorithm
    """
    decompressed_data: bytearray = bytearray()
    position: int = 0

    while position < len(image_data):
        header_byte = image_data[position]
        if header_byte > 127:
            header_byte -= 256
        position += 1

        if 0 <= header_byte <= 127:
            decompressed_data.extend(image_data[position:position + header_byte + 1])
            position += header_byte+1
        elif header_byte == -128:
            pass
        else:
            decompressed_data.extend([image_data[position]] * (1 - header_byte))
            position += 1

    return bytes(decompressed_data)


def compress_packbits(image_data: bytes) -> bytes:
    """
    Compresses the input bytes using the PackBits algorithm
    """
    if not image_data:
        return b''

    compressed_data: bytearray = bytearray()
    i: int = 0

    while i < len(image_data):
        # Look for runs of repeated bytes
        run_start = i
        while i + 1 < len(image_data) and image_data[i] == image_data[i + 1] and (i - run_start) < 127:
            i += 1

        if i > run_start:  # We found a run
            compressed_data.append(257 - (i - run_start + 1))  # Encode run length (negative value)
            compressed_data.append(image_data[run_start])
            i += 1
        else:  # Handle non-repeating sequence
            literal_start = i
            while (
                    i < len(image_data)
                    and (i + 1 >= len(image_data) or image_data[i] != image_data[i + 1])
                    and (i - literal_start) < 127
            ):
                i += 1

            compressed_data.append(i - literal_start - 1)  # Encode literal length (positive value)
            compressed_data.extend(image_data[literal_start:i])

    return bytes(compressed_data)
