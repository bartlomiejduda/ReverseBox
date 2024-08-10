"""
Copyright © 2024  Bartłomiej Duda
License: GPL-3.0 License
"""


from reversebox.common.logger import get_logger
from reversebox.image.image_formats import ImageFormats

logger = get_logger(__name__)

# fmt: off


class YUVDecoder:

    def __init__(self):
        pass

    def decode_yuv_image_main(self, image_data: bytes, img_width: int, img_height: int, image_format: ImageFormats):
        if image_format == ImageFormats.YUY2:
            return self.decode_yuy2_image(image_data, img_width, img_height)
        else:
            raise Exception(f"Image format not supported by yuv decoder! Image_format: {image_format}")

    def _decode_yuy2_pixel(self, Y: float, U: float, V: float) -> bytes:
        p = bytearray(4)

        def _round_clamp_int(f: float) -> int:
            i: int = int(f+0.5)
            if i < 0:
                i = 0
            if i > 255:
                i = 255
            return i

        C: float = Y - 16.0
        D: float = U - 128.0
        E: float = V - 128.0

        R: float = 1.164383 * C + 1.596027 * E
        G: float = 1.164383 * C - (0.391762 * D) - (0.812968 * E)
        B: float = 1.164383 * C + 2.017232 * D

        p[0] = _round_clamp_int(R)
        p[1] = _round_clamp_int(G)
        p[2] = _round_clamp_int(B)
        p[3] = 0xFF
        return p

    def decode_yuy2_image(self, image_data: bytes, img_width: int, img_height: int):
        is_width_odd: bool = True if (img_width & 1) else False
        current_yuv_offset: int = 0
        current_pixel_number: int = 0
        output_texture_data = bytearray(img_width * img_height * 4)

        for y in range(img_height):
            for x in range(0, img_width, 2):

                Y0: float = float(image_data[current_yuv_offset])
                U: float = float(image_data[current_yuv_offset + 1])
                Y1: float = float(image_data[current_yuv_offset + 2])
                V: float = float(image_data[current_yuv_offset + 3])

                pixel1 = self._decode_yuy2_pixel(Y0, U, V)
                pixel2 = self._decode_yuy2_pixel(Y1, U, V)
                output_texture_data[current_pixel_number * 4:(current_pixel_number + 1) * 4] = pixel1
                output_texture_data[(current_pixel_number + 1) * 4:(current_pixel_number + 2) * 4] = pixel2

                if is_width_odd and x == img_width - 1:
                    current_yuv_offset += 4
                    current_pixel_number += 1
                else:
                    current_yuv_offset += 4
                    current_pixel_number += 2

        return output_texture_data
