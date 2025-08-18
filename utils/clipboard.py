# youtube_downloader/utils/clipboard.py

def get_clipboard_text(widget):
    """
    Attempts to get text from the clipboard.
    Returns the text or an empty string if it fails.
    """
    try:
        return widget.clipboard_get()
    except Exception:
        return ""

def is_youtube_link(text):
    """
    Simple check to see if the text is a YouTube link.
    """
    text = text.strip()
    return "youtube.com/" in text or "youtu.be/" in text