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

    def _yuv_to_rgb(self, Y, U, V, standard: str = "rec709") -> tuple:
        if standard == "jpeg":  # JPEG (JFIF)
            R = Y + 1.140 * (V - 128)
            G = Y - 0.395 * (U - 128) - 0.581 * (V - 128)
            B = Y + 2.032 * (U - 128)
        elif standard == "rec601":  # REC 601 (SDTV)
            R = Y + 1.403 * (V - 128)
            G = Y - 0.344 * (U - 128) - 0.714 * (V - 128)
            B = Y + 1.770 * (U - 128)
        elif standard == "rec709":  # REC 709 (HDTV)
            R = Y + 1.5748 * (V - 128)
            G = Y - 0.1873 * (U - 128) - 0.4681 * (V - 128)
            B = Y + 1.8556 * (U - 128)
        else:
            raise Exception("Standard not supported!")

        R = self._limit_rgb_value(R)
        G = self._limit_rgb_value(G)
        B = self._limit_rgb_value(B)

        return R, G, B

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

    def _decode_yuv422_yuy2_image(self, image_data: bytes, img_width: int, img_height: int) -> bytes:
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

    def _decode_yuv420_nv12_image(self, image_data: bytes, img_width: int, img_height: int) -> bytes:
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

    def _decode_yuv420_nv21_image(self, image_data: bytes, img_width: int, img_height: int) -> bytes:
        output_texture_data = bytearray(img_width * img_height * 4)

        p: int = img_height
        for i in range(0, img_height, 2):
            for j in range(0, img_width, 2):
                Y00 = float(image_data[i * img_width + j])
                Y01 = float(image_data[i * img_width + j + 1])
                Y10 = float(image_data[(i + 1) * img_width + j])
                Y11 = float(image_data[(i + 1) * img_width + j + 1])
                U = float(image_data[p * img_width + j + 1])
                V = float(image_data[p * img_width + j])

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

    def _decode_yuv422_uyvy_image(self, image_data: bytes, img_width: int, img_height: int) -> bytes:
        output_texture_data = bytearray(img_width * img_height * 4)

        j: int = 0
        for i in range(0, len(image_data), 4):
            U = float(image_data[i])
            Y0 = float(image_data[i + 1])
            V = float(image_data[i + 2])
            Y1 = float(image_data[i + 3])

            R0 = Y0 + 1.140 * (V - 128.0)
            G0 = Y0 - 0.395 * (U - 128.0) - 0.581 * (V - 128.0)
            B0 = Y0 + 2.032 * (U - 128.0)

            R1 = Y1 + 1.140 * (V - 128.0)
            G1 = Y1 - 0.395 * (U - 128.0) - 0.581 * (V - 128.0)
            B1 = Y1 + 2.032 * (U - 128.0)

            output_texture_data[j] = self._limit_rgb_value(R0)
            output_texture_data[j + 1] = self._limit_rgb_value(G0)
            output_texture_data[j + 2] = self._limit_rgb_value(B0)
            output_texture_data[j + 3] = 0xFF

            output_texture_data[j + 4] = self._limit_rgb_value(R1)
            output_texture_data[j + 5] = self._limit_rgb_value(G1)
            output_texture_data[j + 6] = self._limit_rgb_value(B1)
            output_texture_data[j + 7] = 0xFF

            j += 8

        return output_texture_data

    def _decode_yuv444p_image(self, image_data: bytes, img_width: int, img_height: int) -> bytes:
        output_texture_data = bytearray(img_width * img_height * 4)

        num_pixels: int = img_width * img_height
        y_plane_start: int = 0
        u_plane_start: int = num_pixels
        v_plane_start: int = num_pixels * 2

        for i in range(img_height):
            for j in range(img_width):
                y_index = y_plane_start + i * img_width + j
                u_index = u_plane_start + i * img_width + j
                v_index = v_plane_start + i * img_width + j

                Y = image_data[y_index]
                U = image_data[u_index]
                V = image_data[v_index]

                R = Y + 1.140 * (V - 128)
                G = Y - 0.395 * (U - 128) - 0.581 * (V - 128)
                B = Y + 2.032 * (U - 128)

                R = self._limit_rgb_value(R)
                G = self._limit_rgb_value(G)
                B = self._limit_rgb_value(B)

                rgba_index = (i * img_width + j) * 4
                output_texture_data[rgba_index] = R
                output_texture_data[rgba_index + 1] = G
                output_texture_data[rgba_index + 2] = B
                output_texture_data[rgba_index + 3] = 0xFF

        return output_texture_data

    def _decode_yuv410p_image(self, image_data: bytes, img_width: int, img_height: int) -> bytes:
        output_texture_data = bytearray(img_width * img_height * 4)
        num_pixels: int = img_width * img_height
        uv_width: int = img_width // 4
        uv_height: int = img_height // 4
        uv_size: int = uv_width * uv_height

        y_plane_start: int = 0
        u_plane_start: int = num_pixels
        v_plane_start: int = num_pixels + uv_size

        for i in range(img_height):
            for j in range(img_width):
                y_index = y_plane_start + i * img_width + j
                u_index = u_plane_start + (i // 4) * uv_width + (j // 4)
                v_index = v_plane_start + (i // 4) * uv_width + (j // 4)

                Y = image_data[y_index]
                U = image_data[u_index]
                V = image_data[v_index]

                R = Y + 1.140 * (V - 128)
                G = Y - 0.395 * (U - 128) - 0.581 * (V - 128)
                B = Y + 2.032 * (U - 128)

                R = self._limit_rgb_value(R)
                G = self._limit_rgb_value(G)
                B = self._limit_rgb_value(B)

                rgba_index = (i * img_width + j) * 4
                output_texture_data[rgba_index] = R
                output_texture_data[rgba_index + 1] = G
                output_texture_data[rgba_index + 2] = B
                output_texture_data[rgba_index + 3] = 0xFF

        return output_texture_data

    def _decode_yuv420p_image(self, image_data: bytes, img_width: int, img_height: int) -> bytes:
        output_texture_data = bytearray(img_width * img_height * 4)
        num_pixels: int = img_width * img_height
        uv_width: int = img_width // 2
        uv_height: int = img_height // 2
        uv_size: int = uv_width * uv_height

        y_plane_start: int = 0
        u_plane_start: int = num_pixels
        v_plane_start: int = num_pixels + uv_size

        for i in range(img_height):
            for j in range(img_width):
                y_index = y_plane_start + i * img_width + j
                u_index = u_plane_start + (i // 2) * uv_width + (j // 2)
                v_index = v_plane_start + (i // 2) * uv_width + (j // 2)

                Y = image_data[y_index]
                U = image_data[u_index]
                V = image_data[v_index]

                R = Y + 1.140 * (V - 128)
                G = Y - 0.395 * (U - 128) - 0.581 * (V - 128)
                B = Y + 2.032 * (U - 128)

                R = self._limit_rgb_value(R)
                G = self._limit_rgb_value(G)
                B = self._limit_rgb_value(B)

                rgba_index = (i * img_width + j) * 4
                output_texture_data[rgba_index] = R
                output_texture_data[rgba_index + 1] = G
                output_texture_data[rgba_index + 2] = B
                output_texture_data[rgba_index + 3] = 0xFF

        return output_texture_data

    def _decode_yuv422p_image(self, image_data: bytes, img_width: int, img_height: int) -> bytes:
        output_texture_data = bytearray(img_width * img_height * 4)
        num_pixels: int = img_width * img_height
        uv_width: int = img_width // 2
        uv_size: int = uv_width * img_height

        y_plane_start: int = 0
        u_plane_start: int = num_pixels
        v_plane_start: int = num_pixels + uv_size

        for i in range(img_height):
            for j in range(img_width):
                y_index = y_plane_start + i * img_width + j
                u_index = u_plane_start + i * uv_width + (j // 2)
                v_index = v_plane_start + i * uv_width + (j // 2)

                Y = image_data[y_index]
                U = image_data[u_index]
                V = image_data[v_index]

                R = Y + 1.140 * (V - 128)
                G = Y - 0.395 * (U - 128) - 0.581 * (V - 128)
                B = Y + 2.032 * (U - 128)

                R = self._limit_rgb_value(R)
                G = self._limit_rgb_value(G)
                B = self._limit_rgb_value(B)

                rgba_index = (i * img_width + j) * 4
                output_texture_data[rgba_index] = R
                output_texture_data[rgba_index + 1] = G
                output_texture_data[rgba_index + 2] = B
                output_texture_data[rgba_index + 3] = 0xFF

        return output_texture_data

    def _decode_yuv411p_image(self, image_data: bytes, img_width: int, img_height: int) -> bytes:
        output_texture_data = bytearray(img_width * img_height * 4)
        num_pixels: int = img_width * img_height
        uv_width: int = img_width // 4
        uv_size: int = uv_width * img_height

        y_plane_start: int = 0
        u_plane_start: int = num_pixels
        v_plane_start: int = num_pixels + uv_size

        for i in range(img_height):
            for j in range(img_width):
                y_index = y_plane_start + i * img_width + j
                u_index = u_plane_start + i * uv_width + (j // 4)
                v_index = v_plane_start + i * uv_width + (j // 4)

                Y = image_data[y_index]
                U = image_data[u_index]
                V = image_data[v_index]

                R = Y + 1.140 * (V - 128)
                G = Y - 0.395 * (U - 128) - 0.581 * (V - 128)
                B = Y + 2.032 * (U - 128)

                R = self._limit_rgb_value(R)
                G = self._limit_rgb_value(G)
                B = self._limit_rgb_value(B)

                rgba_index = (i * img_width + j) * 4
                output_texture_data[rgba_index] = R
                output_texture_data[rgba_index + 1] = G
                output_texture_data[rgba_index + 2] = B
                output_texture_data[rgba_index + 3] = 0xFF

        return output_texture_data

    def _decode_yuv411_uyyvyy411_image(self, image_data: bytes, img_width: int, img_height: int) -> bytes:
        output_texture_data = bytearray(img_width * img_height * 4)

        def set_pixel(out_rgba_array, row, col, R, G, B):
            out_index = (row * img_width + col) * 4
            out_rgba_array[out_index] = R
            out_rgba_array[out_index + 1] = G
            out_rgba_array[out_index + 2] = B
            out_rgba_array[out_index + 3] = 0xFF

        for i in range(img_height):
            for j in range(0, img_width, 4):
                index: int = int(i * img_width * 1.5 + j * 1.5)

                U = image_data[index]
                Y0 = image_data[index + 1]
                Y1 = image_data[index + 2]
                V = image_data[index + 3]
                Y2 = image_data[index + 4]
                Y3 = image_data[index + 5]

                R0, G0, B0 = self._yuv_to_rgb(Y0, U, V)
                R1, G1, B1 = self._yuv_to_rgb(Y1, U, V)
                R2, G2, B2 = self._yuv_to_rgb(Y2, U, V)
                R3, G3, B3 = self._yuv_to_rgb(Y3, U, V)

                set_pixel(output_texture_data, i, j, R0, G0, B0)
                set_pixel(output_texture_data, i, j + 1, R1, G1, B1)
                set_pixel(output_texture_data, i, j + 2, R2, G2, B2)
                set_pixel(output_texture_data, i, j + 3, R3, G3, B3)

        return output_texture_data

    def _decode_yuv440p_image(self, image_data: bytes, img_width: int, img_height: int) -> bytes:
        output_texture_data = bytearray(img_width * img_height * 4)
        y_plane_size: int = img_width * img_height
        uv_plane_size: int = img_width * (img_height // 2)

        def set_pixel(out_rgba_array, row, col, R, G, B):
            out_index = (row * img_width + col) * 4
            out_rgba_array[out_index] = R
            out_rgba_array[out_index + 1] = G
            out_rgba_array[out_index + 2] = B
            out_rgba_array[out_index + 3] = 0xFF

        y_plane = image_data[0:y_plane_size]
        u_plane = image_data[y_plane_size:y_plane_size + uv_plane_size]
        v_plane = image_data[y_plane_size + uv_plane_size:y_plane_size + 2 * uv_plane_size]

        for i in range(img_height):
            for j in range(img_width):
                Y = y_plane[i * img_width + j]
                U = u_plane[(i // 2) * img_width + j]
                V = v_plane[(i // 2) * img_width + j]

                R, G, B = self._yuv_to_rgb(Y, U, V)
                set_pixel(output_texture_data, i, j, R, G, B)

        return output_texture_data

    def _decode_yuva420p_image(self, image_data: bytes, img_width: int, img_height: int) -> bytes:
        output_texture_data = bytearray(img_width * img_height * 4)
        y_plane_size: int = img_width * img_height
        uv_plane_size: int = (img_width // 2) * (img_height // 2)

        def set_pixel(out_rgba_array, row, col, R, G, B, A):
            out_index = (row * img_width + col) * 4
            out_rgba_array[out_index] = R
            out_rgba_array[out_index + 1] = G
            out_rgba_array[out_index + 2] = B
            out_rgba_array[out_index + 3] = A

        y_plane = image_data[0:y_plane_size]
        u_plane = image_data[y_plane_size:y_plane_size + uv_plane_size]
        v_plane = image_data[y_plane_size + uv_plane_size:y_plane_size + 2 * uv_plane_size]
        a_plane = image_data[y_plane_size + 2 * uv_plane_size:]

        for i in range(img_height):
            for j in range(img_width):
                Y = y_plane[i * img_width + j]
                U = u_plane[(i // 2) * (img_width // 2) + (j // 2)]
                V = v_plane[(i // 2) * (img_width // 2) + (j // 2)]
                A = a_plane[i * img_width + j]
                R, G, B = self._yuv_to_rgb(Y, U, V)
                set_pixel(output_texture_data, i, j, R, G, B, A)

        return output_texture_data

    def _decode_ayuv_image(self, image_data: bytes, img_width: int, img_height: int) -> bytes:
        output_texture_data = bytearray(img_width * img_height * 4)

        for i in range(img_height * img_width):
            V, U, Y, A = image_data[i * 4:i * 4 + 4]
            R, G, B = self._yuv_to_rgb(Y, U, V)
            output_texture_data[i * 4:i * 4 + 4] = R, G, B, A

        return output_texture_data

    def decode_yuv_image_main(self, image_data: bytes, img_width: int, img_height: int, image_format: ImageFormats) -> bytes:
        self._check_if_yuv_image_dimensions_are_correct(img_width, img_height)

        if image_format == ImageFormats.YUV422_YUY2:
            return self._decode_yuv422_yuy2_image(image_data, img_width, img_height)
        elif image_format == ImageFormats.YUV420_NV12:
            return self._decode_yuv420_nv12_image(image_data, img_width, img_height)
        elif image_format == ImageFormats.YUV420_NV21:
            return self._decode_yuv420_nv21_image(image_data, img_width, img_height)
        elif image_format == ImageFormats.YUV422_UYVY:
            return self._decode_yuv422_uyvy_image(image_data, img_width, img_height)
        elif image_format == ImageFormats.YUV444P:
            return self._decode_yuv444p_image(image_data, img_width, img_height)
        elif image_format == ImageFormats.YUV410P:
            return self._decode_yuv410p_image(image_data, img_width, img_height)
        elif image_format == ImageFormats.YUV420P:
            return self._decode_yuv420p_image(image_data, img_width, img_height)
        elif image_format == ImageFormats.YUV422P:
            return self._decode_yuv422p_image(image_data, img_width, img_height)
        elif image_format == ImageFormats.YUV411P:
            return self._decode_yuv411p_image(image_data, img_width, img_height)
        elif image_format == ImageFormats.YUV411_UYYVYY411:
            return self._decode_yuv411_uyyvyy411_image(image_data, img_width, img_height)
        elif image_format == ImageFormats.YUV440P:
            return self._decode_yuv440p_image(image_data, img_width, img_height)
        elif image_format == ImageFormats.YUVA420P:
            return self._decode_yuva420p_image(image_data, img_width, img_height)
        elif image_format == ImageFormats.AYUV:
            return self._decode_ayuv_image(image_data, img_width, img_height)
        else:
            raise Exception(f"Image format not supported by yuv decoder! Image_format: {image_format}")
