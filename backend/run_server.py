import sys
import io
import logging

# Fix for PyInstaller --windowed mode: redirect None stdout/stderr before any imports
class DummyStream(io.RawIOBase):
    encoding = 'utf-8'
    errors = 'replace'
    def write(self, *args, **kwargs): return 0
    def read(self, *args, **kwargs): return b''
    def isatty(self): return False
    def readable(self): return False
    def writable(self): return True
    def seekable(self): return False

if sys.stdout is None:
    sys.stdout = io.TextIOWrapper(DummyStream(), encoding='utf-8', errors='replace')
if sys.stderr is None:
    sys.stderr = io.TextIOWrapper(DummyStream(), encoding='utf-8', errors='replace')
sys.__stdout__ = sys.stdout
sys.__stderr__ = sys.stderr

logging.disable(logging.CRITICAL)

SILENT_LOG_CONFIG = {
    "version": 1,
    "disable_existing_loggers": True,
    "handlers": {"null": {"class": "logging.NullHandler"}},
    "loggers": {
        "uvicorn":        {"handlers": ["null"], "level": "CRITICAL", "propagate": False},
        "uvicorn.error":  {"handlers": ["null"], "level": "CRITICAL", "propagate": False},
        "uvicorn.access": {"handlers": ["null"], "level": "CRITICAL", "propagate": False},
    },
    "root": {"handlers": ["null"], "level": "CRITICAL"},
}

import threading
import webbrowser
import time
import tkinter as tk
from tkinter import font as tkfont
import uvicorn
import main

SERVER_URL = "http://localhost:8000"

def run_server():
    uvicorn.run(main.app, host="0.0.0.0", port=8000, log_config=SILENT_LOG_CONFIG)

def open_browser():
    webbrowser.open(SERVER_URL)

def create_window():
    root = tk.Tk()
    root.title("Xếp Lịch Thể Thao")
    root.geometry("360x200")
    root.resizable(False, False)

    # Colors
    BG = "#1a1a2e"
    ACCENT = "#e94560"
    TEXT = "#eaeaea"
    BTN_BG = "#16213e"

    root.configure(bg=BG)

    # Title
    title_font = tkfont.Font(family="Segoe UI", size=13, weight="bold")
    sub_font   = tkfont.Font(family="Segoe UI", size=9)
    btn_font   = tkfont.Font(family="Segoe UI", size=10, weight="bold")

    tk.Label(root, text="⚽  Xếp Lịch Thể Thao", font=title_font,
             bg=BG, fg=ACCENT).pack(pady=(22, 4))

    tk.Label(root, text=f"Server đang chạy tại  {SERVER_URL}", font=sub_font,
             bg=BG, fg=TEXT).pack(pady=(0, 18))

    # Status dot
    status_frame = tk.Frame(root, bg=BG)
    status_frame.pack()
    tk.Label(status_frame, text="●", font=tkfont.Font(size=10),
             bg=BG, fg="#00e676").pack(side="left")
    tk.Label(status_frame, text="  Đang hoạt động", font=sub_font,
             bg=BG, fg=TEXT).pack(side="left")

    # Buttons
    btn_frame = tk.Frame(root, bg=BG)
    btn_frame.pack(pady=16)

    tk.Button(btn_frame, text="🌐  Mở trình duyệt", font=btn_font,
              bg=ACCENT, fg="white", relief="flat", padx=14, pady=6,
              cursor="hand2", command=open_browser).pack(side="left", padx=8)

    def on_quit():
        root.destroy()
        sys.exit(0)

    tk.Button(btn_frame, text="✕  Tắt server", font=btn_font,
              bg=BTN_BG, fg=TEXT, relief="flat", padx=14, pady=6,
              cursor="hand2", command=on_quit).pack(side="left", padx=8)

    root.protocol("WM_DELETE_WINDOW", on_quit)
    return root

if __name__ == "__main__":
    # Start server in background thread
    server_thread = threading.Thread(target=run_server, daemon=True)
    server_thread.start()

    # Wait a bit then open browser
    threading.Thread(target=lambda: (time.sleep(2), open_browser()), daemon=True).start()

    # Show control window (this blocks until window is closed)
    window = create_window()
    window.mainloop()
