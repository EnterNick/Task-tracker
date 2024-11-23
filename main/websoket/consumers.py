from channels.generic.websocket import AsyncWebsocketConsumer
import json


class NotificationConsumer(AsyncWebsocketConsumer):
    """
    Асинхронный WebSocket-потребитель для отправки уведомлений.

    Этот потребитель обрабатывает подключение, отключение и получение сообщений от WebSocket-клиентов.
    Он использует группы каналов для рассылки уведомлений всем подключенным клиентам.
    """

    async def websocket_connect(self, event):
        self.room_name = self.scope['url_route']['kwargs']['pk']
        self.room_group_name = f'notification_{self.room_name}'

        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']

        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'notification.message',
                'message': message,
            }
        )

    async def notification_message(self, event):
        message = event['message']

        await self.send(text_data=json.dumps({
            'message': message
        }))
