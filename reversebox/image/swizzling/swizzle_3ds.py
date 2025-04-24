"""
Copyright © 2024-2025  Bartłomiej Duda
License: GPL-3.0 License
"""

# Nintendo 3DS Swizzling
# Can occur in:
# - some MT Framework games on 3DS
# - "Mario & Luigi: Superstar Saga + Bowser's Minions" (3DS)
# - BFLIM image files

# fmt: off


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
