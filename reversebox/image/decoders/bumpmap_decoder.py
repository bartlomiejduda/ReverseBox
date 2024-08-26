"""
Copyright © 2024  Bartłomiej Duda
License: GPL-3.0 License
"""
import math

from reversebox.common.logger import get_logger
from reversebox.image.image_formats import ImageFormats

logger = get_logger(__name__)

# fmt: off


class BumpmapDecoder:

    def __init__(self):
        pass

    # 16-bit normal map. Each texel consist of a pair of 8-bit values (S and R)
    # which represent a normal in spherical coordinates.
    # S = polar angle. 0-255 maps to 0-89 degrees.
    # R = azimuthal angle. 0-255 maps to 0-359 degrees.
    # Used in DTEX Texconv Tool
    def _decode_bumpmap_sr_image(self, image_data: bytes, img_width: int, img_height: int) -> bytes:
        rgba_data = bytearray(img_width * img_height * 4)

        for i in range(img_width * img_height):
            S = image_data[i * 2]
            R = image_data[i * 2 + 1]

            polar_angle = S * 89.0 / 255.0
            azimuthal_angle = R * 359.0 / 255.0

            polar_radians = math.radians(polar_angle)
            azimuthal_radians = math.radians(azimuthal_angle)

            nx = math.sin(polar_radians) * math.cos(azimuthal_radians)
            ny = math.sin(polar_radians) * math.sin(azimuthal_radians)
            nz = math.cos(polar_radians)

            r_value = int((nx + 1.0) * 127.5)
            g_value = int((ny + 1.0) * 127.5)
            b_value = int((nz + 1.0) * 127.5)

            rgba_data[i * 4] = r_value
            rgba_data[i * 4 + 1] = g_value
            rgba_data[i * 4 + 2] = b_value
            rgba_data[i * 4 + 3] = 0xFF

        return rgba_data

    def decode_bumpmap_image_main(self, image_data: bytes, img_width: int, img_height: int, image_format: ImageFormats) -> bytes:

        if image_format == ImageFormats.BUMPMAP_SR:
            return self._decode_bumpmap_sr_image(image_data, img_width, img_height)
        else:
            raise Exception(f"Image format not supported by BUMPMAP decoder! Image_format: {image_format}")
