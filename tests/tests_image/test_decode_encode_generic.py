"""
Copyright © 2024-2025  Bartłomiej Duda
License: GPL-3.0 License
"""

import os
import platform
import time
from typing import List

import matplotlib.pyplot as plt
import pytest

from reversebox.image.image_decoder import ImageDecoder
from reversebox.image.image_encoder import ImageEncoder
from reversebox.image.image_formats import ImageFormats
from reversebox.image.pillow_wrapper import PillowWrapper
from tests.common import ImageDecodeEncodeTestEntry, ImagePerformanceTestEntry

# fmt: off


def _get_test_image_path(file_name: str) -> str:
    return os.path.join(os.path.dirname(__file__), f"image_files/{file_name}")


@pytest.mark.imagetest
def test_decode_and_encode_all_generic_images():

    image_decoder = ImageDecoder()
    image_encoder = ImageEncoder()
    wrapper = PillowWrapper()

    image_test_entries = [
        ImageDecodeEncodeTestEntry(img_file_path="monkey_RGBA8888.bin", debug_flag=False, img_width=256, img_height=128, img_format=ImageFormats.RGBA8888),
        ImageDecodeEncodeTestEntry(img_file_path="monkey_BGR565.bin", debug_flag=False, img_width=256, img_height=128, img_format=ImageFormats.BGR565),
        ImageDecodeEncodeTestEntry(img_file_path="monkey_BGRA8888.bin", debug_flag=False, img_width=256, img_height=128, img_format=ImageFormats.BGRA8888),
        ImageDecodeEncodeTestEntry(img_file_path="monkey_RGB565.bin", debug_flag=False, img_width=256, img_height=128, img_format=ImageFormats.RGB565),
        ImageDecodeEncodeTestEntry(img_file_path="monkey_RGB888.bin", debug_flag=False, img_width=256, img_height=128, img_format=ImageFormats.RGB888),
        ImageDecodeEncodeTestEntry(img_file_path="monkey_BGR888.bin", debug_flag=False, img_width=256, img_height=128, img_format=ImageFormats.BGR888),
        ImageDecodeEncodeTestEntry(img_file_path="monkey_ABGR4444.bin", debug_flag=False, img_width=256, img_height=128, img_format=ImageFormats.ABGR4444),
        ImageDecodeEncodeTestEntry(img_file_path="monkey_BGRA4444.bin", debug_flag=False, img_width=256, img_height=128, img_format=ImageFormats.BGRA4444),
    ]

    performance_test_entries: List[ImagePerformanceTestEntry] = []
    PERFORMANCE_TEST_COUNT: int = 5
    PERFORMANCE_TEST_FLAG: bool = False
    PERFORMANCE_TEST_ID: int = 0

    for test_entry in image_test_entries:

        bin_file = open(_get_test_image_path(test_entry.img_file_path), "rb")
        encoded_image_data = bin_file.read()
        bin_file.close()
        decoded_image_data: bytes = image_decoder.decode_image(encoded_image_data, test_entry.img_width, test_entry.img_height, test_entry.img_format)
        re_encoded_image_data: bytes = image_encoder.encode_image(decoded_image_data, test_entry.img_width, test_entry.img_height, test_entry.img_format)
        re_decoded_image_data: bytes = image_decoder.decode_image(re_encoded_image_data, test_entry.img_width, test_entry.img_height, test_entry.img_format)

        # performance test logic start ###################################################################################
        if PERFORMANCE_TEST_FLAG:
            PERFORMANCE_TEST_ID += 1
            start_time = time.time()
            for i in range(PERFORMANCE_TEST_COUNT):
                bin_file = open(_get_test_image_path(test_entry.img_file_path), "rb")
                encoded_image_data = bin_file.read()
                bin_file.close()
                decoded_image_data: bytes = image_decoder.decode_image(encoded_image_data, test_entry.img_width, test_entry.img_height, test_entry.img_format)
                re_encoded_image_data: bytes = image_encoder.encode_image(decoded_image_data, test_entry.img_width, test_entry.img_height, test_entry.img_format)
                re_decoded_image_data: bytes = image_decoder.decode_image(re_encoded_image_data, test_entry.img_width, test_entry.img_height, test_entry.img_format)
            execution_time = round(time.time() - start_time, 2)
            performance_test_entries.append(ImagePerformanceTestEntry(
                test_id=PERFORMANCE_TEST_ID,
                img_format=test_entry.img_format,
                execution_time=execution_time
            ))
        # performance test logic end ######################################################################################

        # debug start ###############################################################################################
        if test_entry.debug_flag:
            pil_image = wrapper.get_pillow_image_from_rgba8888_data(re_decoded_image_data, test_entry.img_width, test_entry.img_height)
            pil_image.show()
        # debug end #################################################################################################

        assert len(encoded_image_data) > 0
        assert len(decoded_image_data) > 0
        assert len(re_encoded_image_data) > 0
        assert len(re_decoded_image_data) > 0
        assert len(decoded_image_data) == len(re_decoded_image_data)
        assert len(encoded_image_data) == len(re_encoded_image_data)

        assert decoded_image_data[:100] == re_decoded_image_data[:100]
        assert decoded_image_data[1000:1100] == re_decoded_image_data[1000:1100]
        assert decoded_image_data[3000:3100] == re_decoded_image_data[3000:3100]
        assert decoded_image_data[-100:] == re_decoded_image_data[-100:]

        assert encoded_image_data[:100] == re_encoded_image_data[:100]
        assert encoded_image_data[1000:1100] == re_encoded_image_data[1000:1100]
        assert encoded_image_data[3000:3100] == re_encoded_image_data[3000:3100]
        assert encoded_image_data[-100:] == re_encoded_image_data[-100:]

    if PERFORMANCE_TEST_FLAG:
        left = [test_result.test_id for test_result in performance_test_entries]
        time_results = [test_result.execution_time for test_result in performance_test_entries]
        tick_label = [test_result.img_format.value for test_result in performance_test_entries]
        plt.bar(left, time_results, tick_label=tick_label, width=0.8, color=['green'])

        plt.xlabel('')
        plt.ylabel('time in seconds')
        plt.title(f'ReverseBox decode/encode image performance tests (Python {platform.python_version()})')
        plt.xticks(rotation=90)
        plt.gcf().subplots_adjust(bottom=0.2)
        plt.show()
