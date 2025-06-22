"""
Copyright © 2022-2025  Bartłomiej Duda
License: GPL-3.0 License
"""

import logging


class LazyFileHandler(logging.FileHandler):
    def __init__(self, filename, mode="a", encoding=None, delay=True):
        super().__init__(filename, mode, encoding, delay)
        self.has_written = False

    def emit(self, record):
        if not self.has_written:
            if self.stream is None:
                self.stream = self._open()
            self.has_written = True
        super().emit(record)


def get_logger(name):
    logger = logging.getLogger(name)

    c_handler = logging.StreamHandler()
    f_handler = LazyFileHandler("log.txt")
    logger.setLevel(logging.DEBUG)

    log_format = (
        "%(asctime)s - %(name)s - line %(lineno)d - %(levelname)s - %(message)s"
    )
    datetime_format = "%Y-%m-%d %H:%M:%S"
    c_format = logging.Formatter(log_format, datetime_format)
    f_format = logging.Formatter(log_format, datetime_format)
    c_handler.setFormatter(c_format)
    f_handler.setFormatter(f_format)

    logger.addHandler(c_handler)
    logger.addHandler(f_handler)

    return logger
