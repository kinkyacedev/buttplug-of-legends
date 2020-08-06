import asyncio
import time
from queue import Queue, Empty
from threading import Thread
from buttplug.client import ButtplugClientDevice
from patterns import Stop


class Buttplug_Thread(Thread):
    def __init__(self, queue: Queue, device: ButtplugClientDevice):
        self.queue = queue
        self.patterns: list = []
        self.device = device
        super().__init__()

    def run(self):
        coroutine = self.true_function()
        loop = asyncio.get_event_loop()
        try:
            loop.run_until_complete(coroutine)
        except KeyboardInterrupt:
            print("BP THREAD: Received exit, exiting")
            
    async def true_function(self):
        while True:
            try:
                pattern = self.queue.get_nowait()
                if isinstance(pattern, Stop):
                    self.patterns.clear()
                    await self.device.send_stop_device_cmd()
            except Empty:
                pass
            if len(self.patterns) > 0:
                speed = self.patterns[0].next()
                if speed is None:
                    self.patterns.pop(0)
                    continue
                await self.device.send_vibrate_cmd(speed)
            time.sleep(0.25)
