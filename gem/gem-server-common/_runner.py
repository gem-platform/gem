"""Restarts application if any file changed."""
import time

from watchdog.events import PatternMatchingEventHandler
from watchdog.observers import Observer

process = None


def restart():
    global process
    import subprocess

    if process:
        process.terminate()
        returncode = process.kill()
        print("Returncode of subprocess: %s" % returncode)

    process = subprocess.Popen(["python3", "../app/main.py"])
    print("Process ID of subprocess %s" % process.pid)


class MyHandler(PatternMatchingEventHandler):
    def __init__(self):
        super().__init__(
            patterns=["*.py"],
            ignore_patterns=["process.py"])

    def on_any_event(self, event):
        print(event)
        restart()


if __name__ == "__main__":
    restart()

    event_handler = MyHandler()
    observer = Observer()
    observer.schedule(event_handler, path='.', recursive=True)
    observer.start()

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()
