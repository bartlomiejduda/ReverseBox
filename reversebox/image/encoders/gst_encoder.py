"""
Copyright © 2024  Bartłomiej Duda
License: GPL-3.0 License
"""

from reversebox.common.logger import get_logger
from reversebox.image.image_formats import ImageFormats

logger = get_logger(__name__)

# fmt: off


class GSTImageEncoder:
    """
    Encoder for any PS2 GST images
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

    def encode_gst_image_main(self, image_data: bytes, img_width: int, img_height: int, image_format: ImageFormats, is_swizzled: bool) -> bytes:
        block_width, block_height, detail_bpp = self.gst_data_formats[image_format]

        # TODO
        return b''
