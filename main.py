# youtube_downloader/main.py

import ttkbootstrap as b
from gui.app_gui import AppGUI
from gui.theme_manager import apply_theme
from utils import settings

def main():
    # Create the main window using ttkbootstrap
    root = b.Window(themename=settings.DEFAULT_THEME)
    
    # Create the application GUI
    app = AppGUI(root)
    
    # Run the main event loop
    root.mainloop()

if __name__ == "__main__":
    main()