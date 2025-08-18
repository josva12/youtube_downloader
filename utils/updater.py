# youtube_downloader/utils/updater.py

import subprocess
import sys
import threading
from tkinter import messagebox

def check_for_yt_dlp_update():
    """
    Runs 'yt-dlp -U' in a separate thread and shows a message if it was updated.
    This prevents the GUI from freezing.
    """
    def run_update():
        try:
            # Determine the correct Python executable
            python_executable = sys.executable
            
            # Execute the command
            result = subprocess.run(
                [python_executable, "-m", "yt_dlp", "-U"],
                capture_output=True,
                text=True,
                check=True,
                creationflags=subprocess.CREATE_NO_WINDOW if sys.platform == 'win32' else 0
            )
            
            output = result.stdout
            if "is up to date" in output:
                # Optionally, show a message confirming it's up to date
                # messagebox.showinfo("yt-dlp Updater", "yt-dlp is already the latest version.")
                print("yt-dlp is up to date.")
            else:
                messagebox.showinfo("yt-dlp Updater", f"yt-dlp has been updated!\n\n{output}")

        except subprocess.CalledProcessError as e:
            messagebox.showerror("yt-dlp Updater", f"Failed to check for yt-dlp updates.\nError: {e.stderr}")
        except FileNotFoundError:
             messagebox.showerror("yt-dlp Updater", "Failed to check for yt-dlp updates. Is Python in your PATH?")


    # Run the update check in a separate thread to avoid freezing the GUI
    update_thread = threading.Thread(target=run_update)
    update_thread.daemon = True
    update_thread.start()