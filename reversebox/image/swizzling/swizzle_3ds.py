# TODO - refactor this
# fmt: off
def unswizzle_3ds(buffer, width, height):
    bpp: int = 24
    l: int = 8
    m: int = 4
    s: int = 2
    strip_size: int = bpp * s // 8

    unswizzled_data = bytearray(width * height * bpp // 8)
    ptr = 0

    for y in range(0, height, l):
        for x in range(0, width, l):
            for y1 in range(0, l, m):
                for x1 in range(0, l, m):
                    for y2 in range(0, m, s):
                        for x2 in range(0, m, s):
                            for y3 in range(s):
                                idx = (((y + y1 + y2 + y3) * width) + x + x1 + x2) * bpp // 8
                                unswizzled_data[idx: idx+strip_size] = buffer[ptr: ptr+strip_size]
                                ptr += strip_size

    return unswizzled_data
# fmt: on
