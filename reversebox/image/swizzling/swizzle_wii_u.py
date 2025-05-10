"""
Copyright © 2025  Bartłomiej Duda
License: GPL-3.0 License
"""

from typing import List

# WII U Texture Swizzling

# Used in:
# - Mario Kart 8 (WII U)(*.GTX)


# fmt: off


BCn_formats: List[int] = [0x31,   # GX2_SURFACE_FORMAT_T_BC1_UNORM
                          0x431,  # GX2_SURFACE_FORMAT_T_BC1_SRGB
                          0x32,   # GX2_SURFACE_FORMAT_T_BC2_UNORM
                          0x432,  # GX2_SURFACE_FORMAT_T_BC2_SRGB
                          0x33,   # GX2_SURFACE_FORMAT_T_BC3_UNORM
                          0x433,  # GX2_SURFACE_FORMAT_T_BC3_SRGB
                          0x34,   # GX2_SURFACE_FORMAT_T_BC4_UNORM
                          0x234,  # GX2_SURFACE_FORMAT_T_BC4_SNORM
                          0x35,   # GX2_SURFACE_FORMAT_T_BC5_UNORM
                          0x235   # GX2_SURFACE_FORMAT_T_BC5_SNORM
                          ]


m_banks: int = 4
m_banks_bitcount: int = 2
m_pipes: int = 2
m_pipes_bitcount: int = 1
m_pipe_interleave_bytes: int = 256
m_pipe_interleave_bytes_bitcount: int = 8
m_row_size: int = 2048
m_swap_size: int = 256
m_split_size: int = 2048
m_micro_tile_pixels: int = 8 * 8

format_hw_info: bytes = b"\x00\x00\x00\x01\x08\x03\x00\x01\x08\x01\x00\x01\x00\x00\x00\x01" \
                       b"\x00\x00\x00\x01\x10\x07\x00\x00\x10\x03\x00\x01\x10\x03\x00\x01" \
                       b"\x10\x0B\x00\x01\x10\x01\x00\x01\x10\x03\x00\x01\x10\x03\x00\x01" \
                       b"\x10\x03\x00\x01\x20\x03\x00\x00\x20\x07\x00\x00\x20\x03\x00\x00" \
                       b"\x20\x03\x00\x01\x20\x05\x00\x00\x00\x00\x00\x00\x20\x03\x00\x00" \
                       b"\x00\x00\x00\x00\x00\x00\x00\x01\x20\x03\x00\x01\x00\x00\x00\x01" \
                       b"\x00\x00\x00\x01\x20\x0B\x00\x01\x20\x0B\x00\x01\x20\x0B\x00\x01" \
                       b"\x40\x05\x00\x00\x40\x03\x00\x00\x40\x03\x00\x00\x40\x03\x00\x00" \
                       b"\x40\x03\x00\x01\x00\x00\x00\x00\x80\x03\x00\x00\x80\x03\x00\x00" \
                       b"\x00\x00\x00\x01\x00\x00\x00\x01\x00\x00\x00\x01\x10\x01\x00\x00" \
                       b"\x10\x01\x00\x00\x20\x01\x00\x00\x20\x01\x00\x00\x20\x01\x00\x00" \
                       b"\x00\x01\x00\x01\x00\x01\x00\x00\x00\x01\x00\x00\x60\x01\x00\x00" \
                       b"\x60\x01\x00\x00\x40\x01\x00\x01\x80\x01\x00\x01\x80\x01\x00\x01" \
                       b"\x40\x01\x00\x01\x80\x01\x00\x01\x00\x00\x00\x00\x00\x00\x00\x00" \
                       b"\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00" \
                       b"\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00"


def surfaceGetBitsPerPixel(surfaceFormat: int) -> int:
    hwFormat = surfaceFormat & 0x3F
    bpp = format_hw_info[hwFormat * 4 + 0]
    return bpp


def computeSurfaceThickness(tileMode: int) -> int:
    thickness: int = 1

    if tileMode == 3 or tileMode == 7 or tileMode == 11 or tileMode == 13 or tileMode == 15:
        thickness = 4
    elif tileMode == 16 or tileMode == 17:
        thickness = 8

    return thickness


def computePixelIndexWithinMicroTile(x: int, y: int, bpp: int, tileMode: int, z=0) -> int:
    pixelBit6 = 0
    pixelBit7 = 0
    pixelBit8 = 0
    thickness = computeSurfaceThickness(tileMode)

    if bpp == 0x08:
        pixelBit0 = x & 1
        pixelBit1 = (x & 2) >> 1
        pixelBit2 = (x & 4) >> 2
        pixelBit3 = (y & 2) >> 1
        pixelBit4 = y & 1
        pixelBit5 = (y & 4) >> 2

    elif bpp == 0x10:
        pixelBit0 = x & 1
        pixelBit1 = (x & 2) >> 1
        pixelBit2 = (x & 4) >> 2
        pixelBit3 = y & 1
        pixelBit4 = (y & 2) >> 1
        pixelBit5 = (y & 4) >> 2

    elif bpp == 0x20 or bpp == 0x60:
        pixelBit0 = x & 1
        pixelBit1 = (x & 2) >> 1
        pixelBit2 = y & 1
        pixelBit3 = (x & 4) >> 2
        pixelBit4 = (y & 2) >> 1
        pixelBit5 = (y & 4) >> 2

    elif bpp == 0x40:
        pixelBit0 = x & 1
        pixelBit1 = y & 1
        pixelBit2 = (x & 2) >> 1
        pixelBit3 = (x & 4) >> 2
        pixelBit4 = (y & 2) >> 1
        pixelBit5 = (y & 4) >> 2

    elif bpp == 0x80:
        pixelBit0 = y & 1
        pixelBit1 = x & 1
        pixelBit2 = (x & 2) >> 1
        pixelBit3 = (x & 4) >> 2
        pixelBit4 = (y & 2) >> 1
        pixelBit5 = (y & 4) >> 2

    else:
        pixelBit0 = x & 1
        pixelBit1 = (x & 2) >> 1
        pixelBit2 = y & 1
        pixelBit3 = (x & 4) >> 2
        pixelBit4 = (y & 2) >> 1
        pixelBit5 = (y & 4) >> 2

    if thickness > 1:
        pixelBit6 = z & 1
        pixelBit7 = (z & 2) >> 1

    if thickness == 8:
        pixelBit8 = (z & 4) >> 2

    return ((pixelBit8 << 8) | (pixelBit7 << 7) | (pixelBit6 << 6) |
            32 * pixelBit5 | 16 * pixelBit4 | 8 * pixelBit3 |
            4 * pixelBit2 | pixelBit0 | 2 * pixelBit1)


def computePipeFromCoordWoRotation(x: int, y: int) -> int:
    # hardcoded to assume 2 pipes
    return ((y >> 3) ^ (x >> 3)) & 1


def computeBankFromCoordWoRotation(x: int, y: int) -> int:
    numPipes = m_pipes
    numBanks = m_banks
    bank = 0

    if numBanks == 4:
        bankBit0 = ((y // (16 * numPipes)) ^ (x >> 3)) & 1
        bank = bankBit0 | 2 * (((y // (8 * numPipes)) ^ (x >> 4)) & 1)

    elif numBanks == 8:
        bankBit0a = ((y // (32 * numPipes)) ^ (x >> 3)) & 1
        bank = (bankBit0a | 2 * (((y // (32 * numPipes)) ^ (y // (16 * numPipes) ^ (x >> 4))) & 1) |
                4 * (((y // (8 * numPipes)) ^ (x >> 5)) & 1))

    return bank


def isThickMacroTiled(tileMode: int) -> int:
    thickMacroTiled: int = 0

    if tileMode == 7 or tileMode == 11 or tileMode == 13 or tileMode == 15:
        thickMacroTiled = 1

    return thickMacroTiled


def isBankSwappedTileMode(tileMode: int) -> int:
    bankSwapped = 0

    if tileMode == 8 or tileMode == 9 or tileMode == 10 or tileMode == 11 or tileMode == 14 or tileMode == 15:
        bankSwapped = 1

    return bankSwapped


def computeMacroTileAspectRatio(tileMode: int) -> int:
    ratio: int = 1

    if tileMode == 8 or tileMode == 12 or tileMode == 14:
        ratio = 1
    elif tileMode == 5 or tileMode == 9:
        ratio = 2
    elif tileMode == 6 or tileMode == 10:
        ratio = 4

    return ratio


def computeSurfaceBankSwappedWidth(tileMode: int, bpp: int, pitch: int, numSamples: int = 1) -> int:
    if isBankSwappedTileMode(tileMode) == 0:
        return 0

    numBanks = m_banks
    numPipes = m_pipes
    swapSize = m_swap_size
    rowSize = m_row_size
    splitSize = m_split_size
    groupSize = m_pipe_interleave_bytes
    bytesPerSample = 8 * bpp

    try:
        samplesPerTile = splitSize // bytesPerSample
        slicesPerTile = max(1, numSamples // samplesPerTile)
    except ZeroDivisionError:
        slicesPerTile = 1

    if isThickMacroTiled(tileMode) != 0:
        numSamples = 4

    bytesPerTileSlice = numSamples * bytesPerSample // slicesPerTile

    factor = computeMacroTileAspectRatio(tileMode)
    swapTiles = max(1, (swapSize >> 1) // bpp)

    swapWidth = swapTiles * 8 * numBanks
    heightBytes = numSamples * factor * numPipes * bpp // slicesPerTile
    swapMax = numPipes * numBanks * rowSize // heightBytes
    swapMin = groupSize * 8 * numBanks // bytesPerTileSlice

    bankSwapWidth = min(swapMax, max(swapMin, swapWidth))

    while not bankSwapWidth < (2 * pitch):
        bankSwapWidth >>= 1

    return bankSwapWidth


def AddrLib_computeSurfaceAddrFromCoordLinear(x: int, y: int, bpp: int, pitch: int) -> int:
    rowOffset = y * pitch
    pixOffset = x
    addr = (rowOffset + pixOffset) * bpp
    addr //= 8
    return addr


def AddrLib_computeSurfaceAddrFromCoordMicroTiled(x: int, y: int, bpp: int, pitch: int, tileMode: int) -> int:
    microTileThickness = 1

    if tileMode == 3:
        microTileThickness = 4

    microTileBytes = (m_micro_tile_pixels * microTileThickness * bpp + 7) // 8
    microTilesPerRow = pitch >> 3
    microTileIndexX = x >> 3
    microTileIndexY = y >> 3

    microTileOffset = microTileBytes * (microTileIndexX + microTileIndexY * microTilesPerRow)
    pixelIndex = computePixelIndexWithinMicroTile(x, y, bpp, tileMode)
    pixelOffset = bpp * pixelIndex
    pixelOffset >>= 3
    return pixelOffset + microTileOffset


def AddrLib_computeSurfaceAddrFromCoordMacroTiled(x: int, y: int, bpp: int, pitch: int, height: int, tileMode: int, pipeSwizzle: int, bankSwizzle: int) -> int:
    numPipes = m_pipes
    numBanks = m_banks
    numGroupBits = m_pipe_interleave_bytes_bitcount
    numPipeBits = m_pipes_bitcount
    numBankBits = m_banks_bitcount

    microTileThickness = computeSurfaceThickness(tileMode)

    microTileBits = bpp * (microTileThickness * m_micro_tile_pixels)
    microTileBytes = (microTileBits + 7) // 8

    pixelIndex = computePixelIndexWithinMicroTile(x, y, bpp, tileMode)

    pixelOffset = bpp * pixelIndex

    elemOffset = pixelOffset

    bytesPerSample = microTileBytes
    if microTileBytes <= m_split_size:
        numSamples = 1
        sampleSlice = 0
    else:
        samplesPerSlice = m_split_size // bytesPerSample
        numSampleSplits = max(1, 1 // samplesPerSlice)
        numSamples = samplesPerSlice
        sampleSlice = elemOffset // (microTileBits // numSampleSplits)
        elemOffset %= microTileBits // numSampleSplits
    elemOffset += 7
    elemOffset //= 8

    pipe = computePipeFromCoordWoRotation(x, y)
    bank = computeBankFromCoordWoRotation(x, y)

    bankPipe = pipe + numPipes * bank

    swizzle_ = pipeSwizzle + numPipes * bankSwizzle

    bankPipe ^= numPipes * sampleSlice * ((numBanks >> 1) + 1) ^ swizzle_
    bankPipe %= numPipes * numBanks
    pipe = bankPipe % numPipes
    bank = bankPipe // numPipes

    sliceBytes = (height * pitch * microTileThickness * bpp * numSamples + 7) // 8
    sliceOffset = sliceBytes * (sampleSlice // microTileThickness)

    macroTilePitch = 8 * m_banks
    macroTileHeight = 8 * m_pipes

    if tileMode == 5 or tileMode == 9:  # GX2_TILE_MODE_2D_TILED_THIN4 and GX2_TILE_MODE_2B_TILED_THIN2
        macroTilePitch >>= 1
        macroTileHeight *= 2

    elif tileMode == 6 or tileMode == 10:  # GX2_TILE_MODE_2D_TILED_THIN4 and GX2_TILE_MODE_2B_TILED_THIN4
        macroTilePitch >>= 2
        macroTileHeight *= 4

    macroTilesPerRow = pitch // macroTilePitch
    macroTileBytes = (numSamples * microTileThickness * bpp * macroTileHeight * macroTilePitch + 7) // 8
    macroTileIndexX = x // macroTilePitch
    macroTileIndexY = y // macroTileHeight
    macroTileOffset = (macroTileIndexX + macroTilesPerRow * macroTileIndexY) * macroTileBytes

    if tileMode == 8 or tileMode == 9 or tileMode == 10 or tileMode == 11 or tileMode == 14 or tileMode == 15:
        bankSwapOrder = [0, 1, 3, 2, 6, 7, 5, 4, 0, 0]
        bankSwapWidth = computeSurfaceBankSwappedWidth(tileMode, bpp, pitch)
        swapIndex = macroTilePitch * macroTileIndexX // bankSwapWidth
        bank ^= bankSwapOrder[swapIndex & (m_banks - 1)]

    groupMask = ((1 << numGroupBits) - 1)

    numSwizzleBits = (numBankBits + numPipeBits)

    totalOffset = (elemOffset + ((macroTileOffset + sliceOffset) >> numSwizzleBits))

    offsetHigh = (totalOffset & ~groupMask) << numSwizzleBits
    offsetLow = groupMask & totalOffset

    pipeBits = pipe << numGroupBits
    bankBits = bank << (numPipeBits + numGroupBits)

    return bankBits | pipeBits | offsetLow | offsetHigh


def _convert_wii_u(img_width: int, img_height: int, image_format: int, tile_mode: int, swizzle_type: int, pitch: int, input_data: bytes, swizzle_flag: bool) -> bytes:
    converted_data: bytearray = bytearray(input_data)

    if image_format in BCn_formats:
        img_width = (img_width + 3) // 4
        img_height = (img_height + 3) // 4

    for y in range(img_height):
        for x in range(img_width):
            bpp = surfaceGetBitsPerPixel(image_format)
            pipe_swizzle = (swizzle_type >> 8) & 1
            bank_swizzle = (swizzle_type >> 9) & 3

            if tile_mode == 0 or tile_mode == 1:
                pos = AddrLib_computeSurfaceAddrFromCoordLinear(x, y, bpp, pitch)
            elif tile_mode == 2 or tile_mode == 3:
                pos = AddrLib_computeSurfaceAddrFromCoordMicroTiled(x, y, bpp, pitch, tile_mode)
            else:
                pos = AddrLib_computeSurfaceAddrFromCoordMacroTiled(x, y, bpp, pitch, img_height, tile_mode, pipe_swizzle, bank_swizzle)

            bpp //= 8
            pos_ = (y * img_width + x) * bpp

            if swizzle_flag:
                if (pos < len(input_data)) and (pos_ < len(input_data)):
                    converted_data[pos:pos + bpp] = input_data[pos_:pos_ + bpp]
            else:
                if (pos_ < len(input_data)) and (pos < len(input_data)):
                    converted_data[pos_:pos_ + bpp] = input_data[pos:pos + bpp]

    return converted_data


def swizzle_wii_u(img_width: int, img_height: int, image_format: int, tile_mode: int, swizzle_type: int, pitch: int, input_data: bytes) -> bytes:
    return _convert_wii_u(img_width, img_height, image_format, tile_mode, swizzle_type, pitch, input_data, True)


def unswizzle_wii_u(img_width: int, img_height: int, image_format: int, tile_mode: int, swizzle_type: int, pitch: int, input_data: bytes) -> bytes:
    return _convert_wii_u(img_width, img_height, image_format, tile_mode, swizzle_type, pitch, input_data, False)
