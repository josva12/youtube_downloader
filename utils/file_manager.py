# youtube_downloader/utils/file_manager.py

import os
from tkinter import filedialog

def select_save_path(initial_dir):
    """Opens a dialog to select a directory and returns the path."""
    # The parent window is temporarily hidden to make the dialog modal
    return filedialog.askdirectory(initialdir=initial_dir, title="Select Save Location")

def is_valid_path(path):
    """Checks if a path is a valid, writable directory."""
    return os.path.isdir(path) and os.access(path, os.W_OK)