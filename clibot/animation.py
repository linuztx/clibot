import threading
import time
import sys

# Loading animation
class LoadingAnimation:
    def __init__(self):
        self.symbols = ['⣾', '⣷', '⣯', '⣟', '⡿', '⢿', '⣻', '⣽']
        self.i = 0
        self.running = threading.Event()
        self.thread = None

    def loading_animation(self):
        while self.running.is_set():
            self.i = (self.i + 1) % len(self.symbols)
            if sys.stdout.isatty():
                print('\r\033[K%s ' % self.symbols[self.i], flush=True, end='')
            else:
                break
            time.sleep(0.1)
        if sys.stdout.isatty():
            print('\r\033[K', end='')

    def start(self):
        if sys.stdout.isatty():
            self.running.set()
            self.thread = threading.Thread(target=self.loading_animation)
            self.thread.start()

    def stop(self):
        self.running.clear()
        if self.thread is not None:
            self.thread.join()