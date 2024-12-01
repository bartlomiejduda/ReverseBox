"""
Copyright © 2024  Bartłomiej Duda
License: GPL-3.0 License
"""

# fmt: off

# Morton Order Texture Swizzling (+ rotated by 90 degrees for console's CPU)
# https://en.wikipedia.org/wiki/Z-order_curve
# https://dreamcast.wiki/Twiddling

# Same algorithm is used in Dreamcast and PS Vita consoles
# I've seen it used in Dreamcast DTEX files and in PS Vita GXT files
# example games:
# - Danganronpa: Trigger Happy Havoc (PS Vita) (*.GXT)
# - Danganronpa 2: Goodbye Despair (PS Vita) (*.GXT)
# - Senran Kagura: Shinovi Versus (PS Vita) (*.GXT)


def bsr(x: int) -> int:
    """bit scan reverse"""
    if x == 0:
        raise ValueError("bsr is undefined for 0")
    return x.bit_length() - 1


def enclosing_power_of_2(x: int) -> int:
    """find power of 2 equal or bigger than x"""
    return 1 << (x - 1).bit_length()


def align(value: int, alignment: int) -> int:
    """power of two alignment"""
    return (value + (alignment - 1)) & ~(alignment - 1)


def get_morton_index_psvita_dreamcast(x: int, y: int, width: int, height: int) -> int:
    logW = bsr(width)
    logH = bsr(height)
    d = min(logW, logH)
    index = 0

    for i in range(d):
        index |= ((x & (1 << i)) << (i + 1)) | ((y & (1 << i)) << i)

    if width < height:
        index |= ((y & ~(width - 1)) << d)
    else:
        index |= ((x & ~(height - 1)) << d)

    return index


def _convert_psvita_dreamcast_4bpp(pixel_data: bytes, img_width: int, img_height: int, swizzle_flag: bool) -> bytes:
    converted_data: bytearray = bytearray(len(pixel_data))
    mx = get_morton_index_psvita_dreamcast(img_width - 1, 0, img_width, img_height)
    my = get_morton_index_psvita_dreamcast(0, img_height - 1, img_width, img_height)

    line_stride = align(img_width, 2)

    oy = 0
    for y in range(img_height):
        ox = 0
        for x in range(img_width):
            if not swizzle_flag:
                src_ofs_n = ox + oy
                tgt_ofs_n = y * line_stride + x
            else:
                src_ofs_n = y * line_stride + x
                tgt_ofs_n = ox + oy

            src_ofs = src_ofs_n >> 1
            tgt_ofs = tgt_ofs_n >> 1

            src_shift = (src_ofs_n & 1) << 2
            dst_shift = (tgt_ofs_n & 1) << 2

            n = (pixel_data[src_ofs] >> src_shift) & 0xF
            converted_data[tgt_ofs] = (converted_data[tgt_ofs] & (0xF0 >> dst_shift)) | (n << dst_shift)

            ox = (ox - mx) & mx
        oy = (oy - my) & my

    return converted_data


def _convert_psvita_dreamcast(pixel_data: bytes, img_width: int, img_height: int, bpp: int, swizzle_flag: bool) -> bytes:
    converted_data: bytearray = bytearray(len(pixel_data))
    width_pow2 = enclosing_power_of_2(img_width)
    height_pow2 = enclosing_power_of_2(img_height)

    mx = get_morton_index_psvita_dreamcast(width_pow2 - 1, 0, width_pow2, height_pow2)
    my = get_morton_index_psvita_dreamcast(0, height_pow2 - 1, width_pow2, height_pow2)

    pixel_size = bpp // 8

    oy = 0
    for y in range(img_height):
        ox = 0
        for x in range(img_width):
            src_offset = (ox + oy) * pixel_size
            dest_offset = (y * img_width + x) * pixel_size
            if not swizzle_flag:
                converted_data[dest_offset:dest_offset + pixel_size] = pixel_data[src_offset:src_offset + pixel_size]
            else:
                converted_data[src_offset:src_offset + pixel_size] = pixel_data[dest_offset:dest_offset + pixel_size]

            ox = (ox - mx) & mx
        oy = (oy - my) & my

    return converted_data


def unswizzle_psvita_dreamcast(pixel_data: bytes, img_width: int, img_height: int, bpp: int) -> bytes:
    if bpp == 4:
        return _convert_psvita_dreamcast_4bpp(pixel_data, img_width, img_height, False)
    return _convert_psvita_dreamcast(pixel_data, img_width, img_height, bpp, False)


def swizzle_psvita_dreamcast(pixel_data: bytes, img_width: int, img_height: int, bpp: int) -> bytes:
    if bpp == 4:
        return _convert_psvita_dreamcast_4bpp(pixel_data, img_width, img_height, True)
    return _convert_psvita_dreamcast(pixel_data, img_width, img_height, bpp, True)
