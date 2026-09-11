import uvicorn
from main import app
import multiprocessing
import webbrowser
import threading
import time

def open_browser():
    time.sleep(2)
    webbrowser.open("http://localhost:8000")

if __name__ == '__main__':
    multiprocessing.freeze_support()
    threading.Thread(target=open_browser, daemon=True).start()
    uvicorn.run(app, host="0.0.0.0", port=8000)
