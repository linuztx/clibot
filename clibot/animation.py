import threading
import time
import sys
from typing import List

# Loading animation
class LoadingAnimation:
    """A class to display a loading animation in the console."""

    def __init__(self):
        self.symbols: List[str] = ['⣾', '⣷', '⣯', '⣟', '⡿', '⢿', '⣻', '⣽']
        self.i: int = 0
        self.running: threading.Event = threading.Event()
        self.thread: threading.Thread = None

    def loading_animation(self) -> None:
        """Display the loading animation."""
        while self.running.is_set():
            self.i = (self.i + 1) % len(self.symbols)
            if sys.stdout.isatty():
                print('\r\033[K%s ' % self.symbols[self.i], flush=True, end='')
            else:
                break
            time.sleep(0.1)
        if sys.stdout.isatty():
            print('\r\033[K', end='')

    def start(self) -> None:
        """Start the loading animation."""
        if sys.stdout.isatty():
            self.running.set()
            self.thread = threading.Thread(target=self.loading_animation)
            self.thread.start()

    def stop(self) -> None:
        """Stop the loading animation."""
        self.running.clear()
        if self.thread is not None:
            self.thread.join()