"""
Copyright © 2024  Bartłomiej Duda
License: GPL-3.0 License
"""

from PIL import Image


class PillowWrapper:
    def __init__(self):
        pass

    def get_pillow_image_from_rgba8888_data(
        self, image_data: bytes, img_width: int, img_height: int
    ) -> Image:
        pillow_image: Image = Image.frombuffer(
            "RGBA",
            (int(img_width), int(img_height)),
            image_data,
            "raw",
            "RGBA",
            0,
            1,
        )
        return pillow_image

    def get_pillow_image_from_dxt_data(
        self,
        image_data: bytes,
        img_width: int,
        img_height: int,
        decoder_name: str,
        decoder_arg: int,
    ) -> Image:
        pillow_image: Image = Image.frombuffer(
            "RGBA",
            (img_width, img_height),
            image_data,
            decoder_name,
            decoder_arg,
            "",
        )
        return pillow_image

    def get_image_data_from_pillow_image(self, pillow_image: Image) -> bytes:
        return pillow_image.tobytes()
