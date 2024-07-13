"""
Copyright © 2024  Bartłomiej Duda
License: GPL-3.0 License
"""


from reversebox.common.logger import get_logger
from reversebox.image.image_formats import ImageFormats
from reversebox.image.pillow_wrapper import PillowWrapper

logger = get_logger(__name__)

# fmt: off
# mypy: ignore-errors


class ImageEncoder:

    pillow_wrapper = PillowWrapper()

    def __init__(self):
        pass

    compressed_data_formats = {  # TODO
        # image format: (temp, temp)
        ImageFormats.DXT1: ("temp", 1),
        ImageFormats.DXT3: ("temp", 2),
        ImageFormats.DXT5: ("temp", 3)
    }

    def _encode_compressed(self, image_data: bytes, img_width: int, img_height: int, image_format: tuple) -> bytes:
        # TODO
        return image_data


    def encode_compressed_image(self, image_data: bytes, img_width: int, img_height: int, image_format: ImageFormats) -> bytes:
        # TODO
        return self._encode_compressed(image_data, img_width, img_height, self.compressed_data_formats[image_format])
