"""
Copyright © 2024  Bartłomiej Duda
License: GPL-3.0 License
"""

from reversebox.common.logger import get_logger
from reversebox.image.compression.compression_gst import decompress_gst_image
from reversebox.image.image_formats import ImageFormats
from reversebox.image.swizzling.swizzle_gst import (
    unswizzle_detail1,
    unswizzle_detail2,
    unswizzle_gst_base,
)

logger = get_logger(__name__)

# fmt: off


class GSTImageDecoder:
    """
    Decoder for any PS2 GST images
    """

    def __init__(self):
        pass

    gst_data_formats = {
        # image_format: (block_width, block_height, detail_bpp)
        ImageFormats.GST121: (1, 2, 1),
        ImageFormats.GST221: (2, 2, 1),
        ImageFormats.GST421: (4, 2, 1),
        ImageFormats.GST821: (8, 2, 1),
        ImageFormats.GST122: (1, 2, 2),
        ImageFormats.GST222: (2, 2, 2),
        ImageFormats.GST422: (4, 2, 2),
        ImageFormats.GST822: (8, 2, 2),
    }

    def decode_gst_image_main(self, image_data: bytes, img_width: int, img_height: int, image_format: ImageFormats, is_swizzled: bool) -> bytes:
        block_width, block_height, detail_bpp = self.gst_data_formats[image_format]

        size_of_base: int = (img_width // block_width) * (img_height // block_height)
        size_of_detail: int = img_width * img_height * detail_bpp // 8

        if size_of_base + size_of_detail != len(image_data):
            logger.warning(
                f"Size of image {len(image_data)} is different than combined base and detail size {size_of_base + size_of_detail}!")

        detail_offset: int = (size_of_base + (16 - 1)) & ~(16 - 1)

        base_data: bytes = image_data[:size_of_base]
        detail_data: bytes = image_data[detail_offset: detail_offset + size_of_detail]

        # unswizzle GST data
        if is_swizzled:
            base_data = unswizzle_gst_base(base_data, img_width, img_height, block_width, block_height)
            if detail_bpp == 2:
                detail_data = unswizzle_detail2(detail_data, img_width, img_height)
            else:
                detail_data = unswizzle_detail1(detail_data, img_width, img_height)

        # decompress GST data
        decompressed_texture_data: bytes = decompress_gst_image(base_data, detail_data, img_width, img_height, block_width,
                                                                block_height, detail_bpp)

        return decompressed_texture_data
