"""
Copyright © 2022  Bartłomiej Duda
License: GPL-3.0 License
"""

import os
import tkinter as tk

import center_tk_window

from reversebox.common.logger import get_logger
from reversebox.image.image_finder_gui import ImageFinderGUI

logger = get_logger(__name__)

MAIN_DIRECTORY = os.path.dirname(os.path.abspath(__file__))


def run_image_finder() -> int:

    logger.info("Starting image finder...")

    root = tk.Tk()
    ImageFinderGUI(root, "v1.0", MAIN_DIRECTORY)  # start GUI
    root.lift()
    center_tk_window.center_on_screen(root)
    root.mainloop()

    logger.info("End of image finder main...")
    return 0


if __name__ == "__main__":
    run_image_finder()
