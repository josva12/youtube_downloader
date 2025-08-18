# youtube_downloader/core/error_handler.py

class DownloadError(Exception):
    """Custom exception for download failures."""
    pass

class InvalidURLError(Exception):
    """Custom exception for invalid YouTube URLs."""
    pass

class FFmpegError(Exception):
    """Custom exception for when FFmpeg is not found."""
    pass