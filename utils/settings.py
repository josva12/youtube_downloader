# youtube_downloader/utils/settings.py

import os
from pathlib import Path

# --- General Settings ---
APP_NAME = "Zenith Downloader"
APP_VERSION = "1.0.0"
DEFAULT_THEME = "darkly" # A nice dark theme from ttkbootstrap

# --- Default Paths ---
# Use Path for OS-agnostic path handling
DEFAULT_DOWNLOAD_PATH = str(Path.home() / "Downloads")

# --- Supported Formats ---
SUPPORTED_AUDIO_FORMATS = ["mp3", "wav"]