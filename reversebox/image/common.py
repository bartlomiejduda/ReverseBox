"""
Copyright © 2024-2025  Bartłomiej Duda
License: GPL-3.0 License
"""

from reversebox.image.image_formats import ImageFormats

# fmt: off


def convert_bpp_to_bytes_per_pixel(input_bpp: int) -> int:
    if input_bpp <= 0:
        raise ValueError("Invalid bpp value!")
    elif input_bpp <= 8:
        return 1
    elif input_bpp <= 16:
        return 2
    elif input_bpp <= 24:
        return 3
    elif input_bpp <= 32:
        return 4
    else:
        raise Exception("Not supported bpp value!")


def convert_bpp_to_bytes_per_pixel_float(input_bpp: int) -> float:
    if input_bpp <= 0:
        raise ValueError("Invalid bpp value!")
    return input_bpp / 8


# The stride is the number of bytes from one row of pixels in memory to the next row of pixels in memory.
# Stride is also called pitch. If padding bytes are present, the stride is wider than the width of the image.
# stride = rowbytes = pitch
# stride = (width * bpp) >> 3
def get_stride_value(img_width: int, bpp: int) -> int:
    stride: int = img_width * bpp // 8
    return stride


# img_width = pixels_per_row
def get_img_width_from_stride(stride: int, bpp: int) -> int:
    img_width = stride * 8 // bpp
    return img_width


# used in N64/WII games
def get_storage_wh(
        image_width: int, image_height: int, block_width: int, block_height: int
) -> tuple:
    image_width = (image_width + block_width - 1) // block_width * block_width
    image_height = (image_height + block_height - 1) // block_height * block_height
    return image_width, image_height


# used in N64/WII games
def crop_image(
        image_data: bytes,
        width: int,
        height: int,
        bpp: int,
        new_width: int,
        new_height: int,
) -> bytes:
    if width == new_width and height == new_height:
        return image_data

    cropped_image_data = bytearray(new_width * new_height * bpp // 8)

    lw = min(width, new_width) * bpp // 8

    for y in range(0, min(height, new_height)):
        dst = y * new_width * bpp // 8
        src = y * width * bpp // 8
        cropped_image_data[dst: dst + lw] = image_data[src: src + lw]

    return cropped_image_data


def get_bpp_for_image_format(image_format: ImageFormats) -> int:
    if image_format in (ImageFormats.RGB121,
                        ImageFormats.N64_CMPR,
                        ImageFormats.N64_I4,
                        ImageFormats.BC1_DXT1,
                        ImageFormats.BC4_UNORM,
                        ) or "pal4" in image_format.value.lower():
        return 4
    elif image_format in (ImageFormats.RGBX2222,
                          ImageFormats.RGBA2222,
                          ImageFormats.RGB121_BYTE,
                          ImageFormats.RGB332,
                          ImageFormats.BGR332,
                          ImageFormats.GRAY8,
                          ImageFormats.N64_I8,
                          ImageFormats.N64_IA4,
                          ImageFormats.BC2_DXT3,
                          ImageFormats.R8,
                          ImageFormats.G8,
                          ImageFormats.B8,
                          ImageFormats.BC3_DXT5,
                          ImageFormats.BC5_UNORM,
                          ImageFormats.BC6H_UF16,
                          ImageFormats.BC6H_SF16,
                          ImageFormats.BC7_UNORM,
                          ImageFormats.GST121,
                          ImageFormats.GST221,
                          ImageFormats.GST421,
                          ImageFormats.GST821,
                          ImageFormats.GST122,
                          ImageFormats.GST222,
                          ImageFormats.GST422,
                          ImageFormats.GST822,
                          ) or "pal8" in image_format.value.lower():
        return 8
    elif image_format in (ImageFormats.YUV410P, ):
        return 9
    elif image_format in (ImageFormats.YUV411P,
                          ImageFormats.YUV411_UYYVYY411,
                          ImageFormats.YUV420_NV12,
                          ImageFormats.YUV420_NV21,
                          ImageFormats.YUV420P,
                          ):
        return 12
    elif image_format in (ImageFormats.GRAY8A,
                          ImageFormats.GRAY16,
                          ImageFormats.RGB565,
                          ImageFormats.BGR565,
                          ImageFormats.RGBA4444,
                          ImageFormats.RGBX4444,
                          ImageFormats.BGRA4444,
                          ImageFormats.BGRX4444,
                          ImageFormats.BGRX4444,
                          ImageFormats.ARGB4444,
                          ImageFormats.XRGB4444,
                          ImageFormats.ABGR4444,
                          ImageFormats.XBGR4444,
                          ImageFormats.RGBA5551,
                          ImageFormats.RGBX5551,
                          ImageFormats.BGRA5551,
                          ImageFormats.BGRX5551,
                          ImageFormats.ARGB1555,
                          ImageFormats.XRGB1555,
                          ImageFormats.ABGR1555,
                          ImageFormats.XBGR1555,
                          ImageFormats.N64_RGB5A3,
                          ImageFormats.R16,
                          ImageFormats.G16,
                          ImageFormats.B16,
                          ImageFormats.N64_IA8,
                          ImageFormats.YUV422P,
                          ImageFormats.YUV422_UYVY,
                          ImageFormats.YUV422_YUY2,
                          ImageFormats.YUV440P,
                          ImageFormats.BUMPMAP_SR,
                          ) or "pal16" in image_format.value.lower():
        return 16
    elif image_format in (ImageFormats.YUVA420P, ):
        return 20
    elif image_format in (ImageFormats.RGB888,
                          ImageFormats.BGR888,
                          ImageFormats.YUV444P,
                          ):
        return 24
    elif image_format in (ImageFormats.RGBA8888,
                          ImageFormats.BGRA8888,
                          ImageFormats.ARGB8888,
                          ImageFormats.ABGR8888,
                          ImageFormats.XRGB8888,
                          ImageFormats.RGBX8888,
                          ImageFormats.BGRX8888,
                          ImageFormats.N64_RGBA32,
                          ImageFormats.R32,
                          ImageFormats.G32,
                          ImageFormats.B32,
                          ImageFormats.RGBM8888,
                          ImageFormats.AYUV,
                          ):
        return 32
    elif image_format in (ImageFormats.RGB48,
                          ImageFormats.BGR48,
                          ):
        return 48
    else:
        raise Exception(f"Not supported image format! Format: {image_format}")


def is_compressed_image_format(image_format: ImageFormats) -> bool:
    if image_format in (ImageFormats.BC1_DXT1,
                        ImageFormats.BC2_DXT3,
                        ImageFormats.BC3_DXT5,
                        ImageFormats.BC4_UNORM,
                        ImageFormats.BC5_UNORM,
                        ImageFormats.BC6H_UF16,
                        ImageFormats.BC6H_SF16,
                        ImageFormats.BC7_UNORM,
                        ImageFormats.N64_CMPR
                        ):
        return True
    return False
