"""Restarts application if any file changed."""
import time
from subprocess import Popen

from watchdog.events import PatternMatchingEventHandler
from watchdog.observers import Observer

PROCESS = None


def restart():
    """Restart process."""
    global PROCESS

    # kill previously started process
    if PROCESS:
        PROCESS.terminate()
        PROCESS.kill()
        time.sleep(3)

    PROCESS = Popen(["python3", "../app/main.py"])


class RestartHandler(PatternMatchingEventHandler):
    """Restart handler."""

    def __init__(self):
        """Initializes new instance of the RestartHandler class."""
        super().__init__(
            patterns=["*.py"],
            ignore_patterns=["process.py"])

    def on_any_event(self, event):
        """On any event."""
        restart()


if __name__ == "__main__":
    restart()

    HANDLER = RestartHandler()
    OBSERVER = Observer()
    OBSERVER.schedule(HANDLER, path='.', recursive=True)
    OBSERVER.start()
    OBSERVER.join()
