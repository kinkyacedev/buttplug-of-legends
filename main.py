from buttplug.client import (ButtplugClientWebsocketConnector, ButtplugClient, ButtplugClientDevice,
                             ButtplugClientConnectorError)
from league_thread import League_Thread
from buttplug_thread import Buttplug_Thread
from buttplug_alternatives import CustomWebsocketConnection
import asyncio
from queue import SimpleQueue

devices = []
client: ButtplugClient = None
connector: ButtplugClientWebsocketConnector = None
chosen_device: ButtplugClientDevice = None


def device_added(emitter, dev: ButtplugClientDevice):
    global devices
    devices.append(dev)
    print("Found " + str(dev.name))


def device_removed(emitter, dev_index: ButtplugClientDevice):
    global devices
    device = None
    for dev in devices:
        if dev._index == dev_index:
            device = dev
            devices.remove(device)
            break
    print("Removed " + str(device.name))
    if device == chosen_device:
        print("Removed chosen device")
        loop = asyncio.get_event_loop
        loop.stop()


async def scan_and_pick_device():
    global chosen_device
    while True:
        await client.start_scanning()
        print("Scanning devices...")
        await asyncio.sleep(5)
        await print_available_devices()
        await client.stop_scanning()
        num = input("Choose device, r to refresh: ")
        if num.lower() == "r":
            continue
        chosen_device = devices[int(num)]
        return


async def print_available_devices():
    print("\n\n")
    for i, dev in enumerate(devices):
        print("[{0}] {1}".format(i, str(dev.name)))


async def main():
    global devices
    global client
    global connector
    client = ButtplugClient("League of Legends")
    connector = CustomWebsocketConnection("ws://127.0.0.1:12345")
    client.device_added_handler += device_added
    client.device_removed_handler += device_removed
    try:
        await client.connect(connector)
    except ButtplugClientConnectorError as e:
        print("Could not connect to server, exiting: {}".format(e.message))
        return
    await scan_and_pick_device()
    queue = SimpleQueue()
    queue2 = SimpleQueue()
    lol = League_Thread(queue)
    lol.start()
    bu = Buttplug_Thread(queue, chosen_device, queue2)
    bu.start()
    while True:
        item = queue2.get()
        print(item)
        if item == "stop":
            await chosen_device.send_stop_device_cmd()
        else:
            await chosen_device.send_vibrate_cmd(item)


if __name__ == "__main__":
    coro = main()
    loop = asyncio.get_event_loop()
    try:
        loop.run_until_complete(coro)
    except KeyboardInterrupt:
        print("Received exit, exiting")
