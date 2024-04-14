# fmt: off
def unswizzle_switch(buffer, width, height, bpb, block_height=16, width_pad=16, height_pad=16):
    # setup
    unswizzled_data = bytearray(len(buffer))
    if width % width_pad or height % height_pad:
        width_show = width
        height_show = height
        width = width_real = ((width + width_pad - 1) // width_pad) * width_pad
        height = height_real = ((height + height_pad - 1) // height_pad) * height_pad
    else:
        width_show = width_real = width
        height_show = height_real = height
    image_width_in_gobs = width * bpb // 64

    # unswizzling
    for Y in range(height):
        for X in range(width):
            Z = Y * width + X
            gob_address = 0 + (Y // (8 * block_height)) * 512 * block_height * image_width_in_gobs + (X * bpb // 64) * 512 * block_height + (Y % (8 * block_height) // 8) * 512
            X *= bpb
            address = gob_address + ((X % 64) // 32) * 256 + ((Y % 8) // 2) * 64 + ((X % 32) // 16) * 32 + (Y % 2) * 16 + (X % 16)
            unswizzled_data[Z * bpb:(Z + 1) * bpb] = buffer[address:address + bpb]

    # crop
    if width_show != width_real or height_show != height_real:
        crop = bytearray(width_show * height_show * bpb)
        for Y in range(height_show):
            offset_in = Y * width_real * bpb
            offset_out = Y * width_show * bpb
            crop[offset_out:offset_out + width_show * bpb] = unswizzled_data[offset_in:offset_in + width_show * bpb]
        unswizzled_data = crop

    return unswizzled_data
# fmt: on
