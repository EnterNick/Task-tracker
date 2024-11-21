import json
from channels.generic.websocket import AsyncWebsocketConsumer


class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        await self.channel_layer.group_add("websoket", self.channel_name)
        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard("websoket", self.channel_name)

    async def receive(self, text_data=None, bytes_data=None):
        text_data_json = json.loads(text_data)

        message = text_data_json["message"]

        await self.channel_layer.group_send(
            "websoket", {"type": "chat.message", "message": message, "sender_channel": self.channel_name}
        )

    async def chat_message(self, event):
        message = event["message"]
        ip = self.scope['client'][0]
        await self.send(text_data=json.dumps({"websoket": message, 'ip': ip}))
