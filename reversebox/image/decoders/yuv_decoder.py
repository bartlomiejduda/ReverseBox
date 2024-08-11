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

    def _check_if_yuv_image_dimensions_are_correct(self, img_width: int, img_height: int) -> bool:
        MIN_IMAGE_WIDTH = 4
        MIN_IMAGE_HEIGHT = 4

        if img_width < MIN_IMAGE_WIDTH or img_height < MIN_IMAGE_HEIGHT:
            raise Exception("YUV image to small to convert!")

        return True

    def _limit_rgb_value(self, f: float) -> int:
        i: int = int(f + 0.5)
        if i < 0:
            i = 0
        if i > 255:
            i = 255
        return i

    def _decode_yuy2_pixel(self, Y: float, U: float, V: float) -> bytes:
        p = bytearray(4)

        C: float = Y - 16.0
        D: float = U - 128.0
        E: float = V - 128.0

        R: float = 1.164383 * C + 1.596027 * E
        G: float = 1.164383 * C - (0.391762 * D) - (0.812968 * E)
        B: float = 1.164383 * C + 2.017232 * D

        p[0] = self._limit_rgb_value(R)
        p[1] = self._limit_rgb_value(G)
        p[2] = self._limit_rgb_value(B)
        p[3] = 0xFF
        return p

    def _decode_yuy2_image(self, image_data: bytes, img_width: int, img_height: int):
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

    def _decode_nv12_image(self, image_data: bytes, img_width: int, img_height: int):
        output_texture_data = bytearray(img_width * img_height * 4)

        p: int = img_height
        for i in range(0, img_height, 2):
            for j in range(0, img_width, 2):
                Y00 = float(image_data[i * img_width + j])
                Y01 = float(image_data[i * img_width + j + 1])
                Y10 = float(image_data[(i + 1) * img_width + j])
                Y11 = float(image_data[(i + 1) * img_width + j + 1])
                U = float(image_data[p * img_width + j])
                V = float(image_data[p * img_width + j + 1])

                R = Y00 + 1.140 * (V - 128.0)
                G = Y00 - 0.395 * (U - 128.0) - 0.581 * (V - 128.0)
                B = Y00 + 2.032 * (U - 128.0)
                output_texture_data[i * img_width * 4 + j * 4] = self._limit_rgb_value(R)
                output_texture_data[i * img_width * 4 + j * 4 + 1] = self._limit_rgb_value(G)
                output_texture_data[i * img_width * 4 + j * 4 + 2] = self._limit_rgb_value(B)
                output_texture_data[i * img_width * 4 + j * 4 + 3] = 0xFF

                R = Y01 + 1.140 * (V - 128.0)
                G = Y01 - 0.395 * (U - 128.0) - 0.581 * (V - 128.0)
                B = Y01 + 2.032 * (U - 128.0)
                output_texture_data[i * img_width * 4 + j * 4 + 4] = self._limit_rgb_value(R)
                output_texture_data[i * img_width * 4 + j * 4 + 5] = self._limit_rgb_value(G)
                output_texture_data[i * img_width * 4 + j * 4 + 6] = self._limit_rgb_value(B)
                output_texture_data[i * img_width * 4 + j * 4 + 7] = 0xFF

                R = Y10 + 1.140 * (V - 128.0)
                G = Y10 - 0.395 * (U - 128.0) - 0.581 * (V - 128.0)
                B = Y10 + 2.032 * (U - 128.0)
                output_texture_data[(i + 1) * img_width * 4 + j * 4] = self._limit_rgb_value(R)
                output_texture_data[(i + 1) * img_width * 4 + j * 4 + 1] = self._limit_rgb_value(G)
                output_texture_data[(i + 1) * img_width * 4 + j * 4 + 2] = self._limit_rgb_value(B)
                output_texture_data[(i + 1) * img_width * 4 + j * 4 + 3] = 0xFF

                R = Y11 + 1.140 * (V - 128.0)
                G = Y11 - 0.395 * (U - 128.0) - 0.581 * (V - 128.0)
                B = Y11 + 2.032 * (U - 128.0)
                output_texture_data[(i + 1) * img_width * 4 + j * 4 + 4] = self._limit_rgb_value(R)
                output_texture_data[(i + 1) * img_width * 4 + j * 4 + 5] = self._limit_rgb_value(G)
                output_texture_data[(i + 1) * img_width * 4 + j * 4 + 6] = self._limit_rgb_value(B)
                output_texture_data[(i + 1) * img_width * 4 + j * 4 + 7] = 0xFF

            p += 1

        return output_texture_data

    def decode_yuv_image_main(self, image_data: bytes, img_width: int, img_height: int, image_format: ImageFormats):
        self._check_if_yuv_image_dimensions_are_correct(img_width, img_height)

        if image_format == ImageFormats.YUY2:
            return self._decode_yuy2_image(image_data, img_width, img_height)
        elif image_format == ImageFormats.NV12:
            return self._decode_nv12_image(image_data, img_width, img_height)
        else:
            raise Exception(f"Image format not supported by yuv decoder! Image_format: {image_format}")
