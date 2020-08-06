from buttplug.client import ButtplugClientWebsocketConnector
from buttplug.core import ButtplugMessage
import json


class CustomWebsocketConnection(ButtplugClientWebsocketConnector):
    async def send(self, msg: ButtplugMessage):
        msg_str = msg.as_json()
        msg_str = "[" + msg_str + "]"
        #print(msg_str)
        await self.ws.send(msg_str)
        
    async def _consumer_handler(self):
        # Guessing that this fails out once the websocket disconnects?
        while True:
            try:
                message = await self.ws.recv()
            except Exception as e:
                print("Exiting read loop")
                print(e)
                break
            msg_array = json.loads(message)
            for msg in msg_array:
                bp_msg = ButtplugMessage.from_dict(msg)
                #print(bp_msg)
                await self._notify_observers(bp_msg)
