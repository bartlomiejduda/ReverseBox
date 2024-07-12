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
    ):
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
