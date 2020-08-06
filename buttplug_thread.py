from threading import Thread
from queue import Queue, Empty
import time
from patterns import Pattern


class Buttplug_Thread(Thread):
    def __init__(self, queue: Queue):
        self.queue = queue
        self.patterns = []
        super().__init__()

    def run(self):
        while True:
            try:
                data = self.queue.get_nowait()
                print("BP THREAD:", data)
                time.sleep(0.25)
            except Empty:
                time.sleep(5)
