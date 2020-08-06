import asyncio
import time
from queue import Queue, Empty
from threading import Thread
from buttplug.client import ButtplugClientDevice
from patterns import Stop


class Buttplug_Thread(Thread):
    def __init__(self, queue: Queue, device: ButtplugClientDevice, queue2: Queue):
        self.queue = queue
        self.patterns: list = []
        self.device = device
        self.queue2 = queue2
        super().__init__()

    def run(self):
        while True:
            #print(self.patterns)
            try:
                pattern = self.queue.get_nowait()
                print("got", pattern)
                if isinstance(pattern, Stop):
                    self.patterns.clear()
                    self.queue2.put("stop")
                else:
                    self.patterns.insert(0, pattern)
            except Empty:
                pass
            if len(self.patterns) > 0:
                speed = self.patterns[0].next()
                if speed is None:
                    self.patterns.pop(0)
                    continue
                self.queue2.put(speed)
            else:
                self.queue2.put("stop")
            time.sleep(0.25)
        #coroutine = self.true_function()
        #loop = asyncio.new_event_loop()
        #asyncio.set_event_loop(loop)
        #loop2 = asyncio.get_event_loop()
        #try:
        #    loop.run_until_complete(coroutine)
        #except KeyboardInterrupt:
        #    print("BP THREAD: Received exit, exiting")
    
