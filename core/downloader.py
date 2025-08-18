# youtube_downloader/core/downloader.py

import yt_dlp
import os
from .error_handler import DownloadError, InvalidURLError, FFmpegError

class Downloader:
    def __init__(self, progress_hook):
        self.progress_hook = progress_hook

    def _get_common_ydl_opts(self, save_path):
        return {
            'outtmpl': os.path.join(save_path, '%(title)s.%(ext)s'),
            'progress_hooks': [self.progress_hook],
            'noplaylist': True,
            'quiet': True,
            'noprogress': True, # We use our own progress hook
        }

    def fetch_formats(self, url):
        """Fetches available video formats for a given YouTube URL."""
        try:
            ydl_opts = {'quiet': True, 'noplaylist': True}
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(url, download=False)
                formats = info.get('formats', [])
                
                # Filter for formats with both video and audio, and a decent resolution
                video_formats = [
                    f for f in formats 
                    if f.get('vcodec') != 'none' and f.get('acodec') != 'none' and f.get('height') is not None
                ]
                
                # Create a user-friendly list
                display_formats = {}
                for f in sorted(video_formats, key=lambda x: x.get('height', 0), reverse=True):
                    resolution = f.get('height')
                    fps = f.get('fps')
                    ext = f.get('ext')
                    format_note = f"{resolution}p"
                    if fps:
                        format_note += f" ({fps}fps, {ext})"
                    else:
                        format_note += f" ({ext})"
                    
                    if format_note not in display_formats:
                         display_formats[format_note] = f.get('format_id')
                
                return display_formats
        except yt_dlp.utils.DownloadError as e:
            raise InvalidURLError(f"Invalid or unsupported URL: {url}") from e
        except Exception as e:
            raise DownloadError(f"An unexpected error occurred while fetching formats: {str(e)}") from e


    def download_video(self, url, save_path, format_id):
        """Downloads a video with the specified format ID."""
        ydl_opts = self._get_common_ydl_opts(save_path)
        ydl_opts['format'] = format_id

        try:
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                ydl.download([url])
        except yt_dlp.utils.DownloadError as e:
            raise DownloadError(f"Failed to download video. Please check the URL and your connection.") from e
        except Exception as e:
            raise DownloadError(f"An unexpected error occurred during video download: {str(e)}") from e

    def download_audio(self, url, save_path, audio_format='mp3'):
        """Downloads and converts audio to the specified format."""
        ydl_opts = self._get_common_ydl_opts(save_path)
        ydl_opts['format'] = 'bestaudio/best'
        ydl_opts['postprocessors'] = [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': audio_format,
            'preferredquality': '192' if audio_format == 'mp3' else None,
        }]

        try:
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                ydl.download([url])
        except yt_dlp.utils.PostProcessingError as e:
            raise FFmpegError("FFmpeg not found! Please install FFmpeg and ensure it's in your system's PATH.") from e
        except yt_dlp.utils.DownloadError as e:
            raise DownloadError(f"Failed to download audio. Please check the URL and your connection.") from e
        except Exception as e:
            raise DownloadError(f"An unexpected error occurred during audio download: {str(e)}") from e